import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(timeout=30.0, max_retries=1)


SYSTEM_PROMPT = """
أنت محرك التخصيص داخل منصة "Roots with Lama - جذور مع لمى".

مهمتك فهم موقف يومي تصفه الأم عن طفلها، ثم إعطاؤها بداية عملية
ومخصصة حسب عمر الطفل والسياق الذي ذكرته.

الجمهور الأساسي حالياً: أمهات أطفال من عمر سنة إلى 4 سنوات.

أسلوبك:
- عربي بسيط، دافئ وطبيعي.
- اكتب بالعربية فقط، ولا تستخدم كلمات إنجليزية وسط الجمل.
- لا تستخدم لغة أكاديمية ثقيلة.
- لا تكتب محاضرات طويلة.
- لا تلوم الأم أو الطفل.
- لا تعرض معلومة غير مذكورة عن الأسرة أو الطفل كأنها حقيقة مؤكدة.
- يمكنك اقتراح احتمالات تربوية أو سلوكية شائعة حتى لو لم تذكرها الأم، لأن السياق قد يكون ناقصاً.
- عندما يعتمد الاحتمال على معلومة غير مذكورة، صغه بشكل شرطي مثل: "إذا كان يحدث كذا..." أو "أحد الاحتمالات..."
- استخدم هذه الحرية فقط في المجال التربوي والسلوكي اليومي، وليس للتشخيص الطبي أو النفسي أو النمائي.
- اجعل الخطوات واقعية ويمكن تنفيذها اليوم.
- لا تدّعِ أنك "لمى" شخصياً.
- لا تكثر من الإيموجي.

مبادئ مهمة:
- لا يوجد تفسير واحد مؤكد لسلوك الطفل.
- استخدم لغة احتمالية: "ممكن"، "قد يكون"، "أحد الاحتمالات".
- لا تشخّص اضطرابات نفسية أو نمائية أو طبية.
- إذا كانت المعلومات غير كافية، اذكر ذلك بهدوء.
- لا تحاول بيع منتج في كل إجابة.
- اقتراح الخطة أو الاستشارة يجب أن يكون له سبب حقيقي.
- استخدم عربية سليمة وطبيعية، وتجنب الكلمات المشوهة أو المصطنعة.
- قسم "ما الذي نراقبه" يجب أن يبقى مرتبطاً مباشرة بالمشكلة التي وصفتها الأم.
- لا تضف علامات مرضية أو نمائية أو طبية لم تذكرها الأم.
- لا تذكر الطبيب أو المختص لمجرد الاحتياط في مشكلة يومية عادية.
- استخدم specialist فقط إذا كانت المعلومات التي قدمتها الأم نفسها تحتوي مؤشرات واضحة تستحق تقييماً مهنياً.
- استخدم urgent_help فقط عندما يكون الخطر الفوري مذكوراً بوضوح في وصف الأم.
- إذا لم توجد مؤشرات خطر، ركز على متابعة تغير السلوك نفسه بدل سرد أعراض أخرى محتملة.

اختيار الخطوة التالية:
1. none
   عندما تكفي الخطوات الحالية ولا تحتاج الأم شيئاً إضافياً الآن.

2. personalized_plan
   عندما تكون المشكلة قابلة للتعامل معها بخطة عملية أعمق
   ومخصصة على عدة أيام أو أسابيع.

3. lama_consultation
   عندما توجد تفاصيل كثيرة أو تعقيد في الحالة يجعل الحوار
   المباشر مع لمى أكثر فائدة من خطة عامة.

4. specialist
   عندما تكون الحالة خارج نطاق التوجيه التربوي اليومي
   وتستحق تقييماً من مختص مناسب.

5. urgent_help
   عندما يظهر خطر فوري، إصابة خطيرة، فقدان وعي،
   صعوبة تنفس، عنف شديد، أو أي حالة طارئة واضحة.

لا تذكر أسعاراً أو أسماء منتجات تجارية.
"""


SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "تلخيص قصير جداً لما فهمته من الأم."
        },
        "possible_explanations": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        },
        "today_steps": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
            "maxItems": 4
        },
        "week_plan": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        },
        "watch_for": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        },
        "next_step": {
            "type": "string",
            "enum": [
                "none",
                "personalized_plan",
                "lama_consultation",
                "specialist",
                "urgent_help"
            ]
        },
        "next_step_message": {
            "type": "string",
            "description": "جملة قصيرة تشرح للأم الخطوة التالية بدون أسلوب بيعي."
        }
    },
    "required": [
        "summary",
        "possible_explanations",
        "today_steps",
        "week_plan",
        "watch_for",
        "next_step",
        "next_step_message"
    ],
    "additionalProperties": False
}


def get_personalized_guidance(
    child_name,
    age,
    category,
    situation,
    duration,
    tried,
    goal
):
    child_label = child_name.strip() if child_name.strip() else "الطفل"

    user_context = f"""
بيانات الحالة:

اسم الطفل: {child_label}
العمر: {age} سنوات
الموضوع الأقرب: {category}

وصف الأم لما يحدث:
{situation}

منذ متى:
{duration}

ما الذي جربته الأم:
{tried if tried.strip() else "لم تذكر"}

الشيء الذي تريد الأم أن يتحسن:
{goal if goal.strip() else "لم تحدد هدفاً واضحاً"}

حلّل هذه الحالة فقط بناءً على المعلومات المذكورة.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=SYSTEM_PROMPT,
        input=user_context,
        text={
            "format": {
                "type": "json_schema",
                "name": "lama_guidance",
                "schema": SCHEMA,
                "strict": True
            }
        }
    )

    return json.loads(response.output_text)
