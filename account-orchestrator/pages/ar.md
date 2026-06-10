# account-orchestrator

شغّل عدّة حسابات Claude Code كأنها حوض واحد — استخدام حيّ لكل حساب (5 ساعات / 7 أيام / نسبة لكل
نموذج)، حساب واحد لكل مشروع، وتبديل تلقائي بلا إعادة تحميل لمحادثة قيد التشغيل قبل أن تبلغ
الحد.

## ماذا يفعل
- يجلب الاستخدام **الحيّ** من نقطة OAuth usage → سجلّ صحّة
  (VALID / MAXED / EXPIRED / THROTTLED).
- يوزّع حسابًا مختلفًا لكل نافذة `~/projects/*` (يُكتشف تلقائيًا).
- **يبدّل تلقائيًا** محادثة قيد التشغيل إلى حساب أحدث عند ~90% — **بلا إعادة تحميل للنافذة**
  (تعيد المحادثة قراءة ملف بيانات الاعتماد في رسالتها التالية).
- **يحجز** حسابًا غير متنازَع عليه للمهام الثقيلة probe / research / autopilot.
- لوحة HTML بأشرطة 5 ساعات / 7 أيام + إشارات الحسابات **المفقودة (MISSING)**.

## التثبيت
```bash
curl -fsSL -o account-orchestrator.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/account-orchestrator.tar.gz
tar xzf account-orchestrator.tar.gz
cd account-orchestrator
bash install.sh
```
وثّق كل حساب في مجلّد إعداداته الخاص أولًا (`~/.claude`، `~/.claude-acct1 … N`):
`CLAUDE_CONFIG_DIR=~/.claude-acctN claude /login`.

## الاستخدام
الصِق في Claude Code:
> ثبّت account-orchestrator من الـ Gnesis Vault وأعدّه كي يحصل كل مشروع على حسابه الخاص وتبدّل
> المحادثات قيد التشغيل تلقائيًا قبل بلوغ الحد.

ثم: `claude-acct-status` (السجلّ) · `claude-acct-dashboard` (HTML) ·
`claude-acct-distribute --apply` (حساب واحد لكل مشروع).

## المصدر
https://github.com/primovera12/gnesis-vault/tree/main/account-orchestrator
