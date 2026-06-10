# auto-advance

تبديل واستئناف تلقائي لحسابات Claude Code عند بلوغ حدود الاستخدام/الجلسة. عند توقّف بسبب حد
الاستخدام، يبدّل جلستك إلى أحدث حساب سليم — وفي حلقات الـ headless/autopilot يعيد تشغيل
`claude --continue` كي لا يتوقف العمل. الجلسات التفاعلية في VS Code / CLI تكتفي بالتبديل فقط
حسب التصميم. مبني على `account-orchestrator`.

## ماذا يفعل
- يرصد توقّف حد الاستخدام ويبدّل إلى أحدث حساب (سقف لمنع الاحتكار، تهدئة لمنع التذبذب، ولا
  يبدّل أبدًا إلى حساب مستهلَك بالكامل).
- **Headless / autopilot** (`claude -p`): تلقائي بالكامل — يبدّل **ويعيد** تشغيل
  `claude --continue`.
- **تفاعلي**: تبديل فقط — التبديل فوري، ثم تضغط ↑+Enter للمتابعة على الحساب الجديد. لا يوجد
  استئناف تفاعلي وهمي بدون تدخّل.

## التثبيت
```bash
curl -fsSL -o auto-advance.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/auto-advance.tar.gz
tar xzf auto-advance.tar.gz
cd auto-advance
bash install.sh
```
يتطلّب `jq` و`curl` وأدوات `claude-acct-*` (من `account-orchestrator`).

## الاستخدام
الصِق في Claude Code:
> ثبّت auto-advance من الـ Gnesis Vault ثم شغّله كي يبدّل الـ autopilot الحسابات تلقائيًا عند
> بلوغ الحد.

أو شغّله مباشرة: `/auto-advance start` · `/auto-advance status` · `/auto-advance stop`.

## المصدر
https://github.com/primovera12/gnesis-vault/tree/main/auto-advance
