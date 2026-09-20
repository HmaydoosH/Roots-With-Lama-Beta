import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(timeout=30.0, max_retries=1)


SYSTEM_PROMPT = """
أنت محرك إنشاء الخطط المخصصة داخل منصة
"Roots with Lama - جذور مع لمى".

مهمتك تحويل المعلومات التي شاركتها الأم عن طفلها
إلى خطة عملية قصيرة لمدة 7 أيام.

الجمهور الأساسي حالياً:
أمهات أطفال من عمر سنة إلى 4 سنوات.

الخطة يجب أن تكون:
- مخصصة للحالة المذكورة.
- واقعية وقابلة للتطبيق داخل البيت والحياة اليومية.
- مناسبة للوقت المتاح للأم.
- بسيطة وليست مرهقة.
- متدرجة من يوم إلى آخر.
- مكتوبة بالعربية الطبيعية فقط.
- خالية من المصطلحات الأكاديمية غير الضرورية.
- غير وعظية ولا تلوم الأم أو الطفل.

مهم:
- استخدم كل المعلومات السابقة عن المشكلة، وليس الأسئلة الإضافية فقط.
- لا تكرر نفس النصيحة سبعة أيام بصياغات مختلفة.
- كل يوم يجب أن يبني قليلاً على اليوم السابق.
- لا تجعل الخطة مثالية أو صعبة التنفيذ.
- إذا كان الوقت المتاح 5–10 دقائق، احترم ذلك فعلاً.
- يمكن اقتراح احتمالات تربوية وسلوكية شائعة بصيغة احتمالية أو شرطية.
- لا تعرض معلومات غير مذكورة عن الأسرة كأنها حقائق مؤكدة.
- لا تشخّص حالات طبية أو نفسية أو نمائية.
- لا تستخدم الخطة كبديل لمختص عندما تكون الحالة خارج المجال التربوي اليومي.
- لا تستخدم كلمات إنجليزية وسط الجمل.

فلسفة الخطة:
نريد تغييراً صغيراً ومستداماً،
وليس حلاً سحرياً خلال أسبوع.

كل يوم يجب أن يحتوي:
1. هدف واحد فقط.
2. خطوة رئيسية واضحة.
3. مثال لعبارة يمكن للأم قولها.
4. شيء واحد تراقبه الأم.

وفي نهاية الأسبوع:
- لخص ما نبحث عنه من تقدم.
- اشرح متى نكرر الخطة ومتى نعدّلها.
"""


SCHEMA = {
    "type": "object",
    "properties": {
        "plan_title": {
            "type": "string"
        },
        "plan_goal": {
            "type": "string"
        },
        "before_you_start": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
            "maxItems": 4
        },
        "days": {
            "type": "array",
            "minItems": 7,
            "maxItems": 7,
            "items": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 7
                    },
                    "focus": {
                        "type": "string"
                    },
                    "main_step": {
                        "type": "string"
                    },
                    "say_this": {
                        "type": "string"
                    },
                    "watch_for": {
                        "type": "string"
                    }
                },
                "required": [
                    "day",
                    "focus",
                    "main_step",
                    "say_this",
                    "watch_for"
                ],
                "additionalProperties": False
            }
        },
        "end_of_week": {
            "type": "string"
        },
        "adjustment_note": {
            "type": "string"
        }
    },
    "required": [
        "plan_title",
        "plan_goal",
        "before_you_start",
        "days",
        "end_of_week",
        "adjustment_note"
    ],
    "additionalProperties": False
}


def create_personalized_plan(
    child_name,
    age,
    category,
    situation,
    duration,
    tried,
    goal,
    plan_time,
    plan_context,
    plan_notes
):
    child_label = child_name.strip() if child_name.strip() else "الطفل"

    context = f"""
بيانات الطفل والحالة الأصلية:

اسم الطفل: {child_label}
العمر: {age} سنوات
الموضوع: {category}

ما وصفته الأم:
{situation}

منذ متى:
{duration}

ما الذي جربته:
{tried if tried.strip() else "لم تذكر"}

الهدف الذي تريده الأم:
{goal if goal.strip() else "لم تحدد هدفاً واضحاً"}


معلومات إضافية لبناء الخطة:

الوقت المتاح يومياً:
{plan_time}

متى أو في أي ظروف تحدث المشكلة غالباً:
{plan_context if plan_context.strip() else "لم تذكر"}

أمور مهمة يجب مراعاتها:
{plan_notes if plan_notes.strip() else "لا توجد ملاحظات إضافية"}

أنشئ خطة مخصصة لمدة 7 أيام لهذه الحالة.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=SYSTEM_PROMPT,
        input=context,
        text={
            "format": {
                "type": "json_schema",
                "name": "roots_personalized_plan",
                "schema": SCHEMA,
                "strict": True
            }
        }
    )

    return json.loads(response.output_text)
