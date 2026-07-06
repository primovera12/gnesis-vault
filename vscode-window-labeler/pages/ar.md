# مُسمِّي نوافذ VS Code

امنح كل نافذة من نوافذ VS Code اسماً مرئياً **ولوناً مميزاً** لشريط العنوان، بحيث يمكنك تمييز مشاريعك بنظرة واحدة — حتى من شريط المهام.

## ما يفعله

- **التسمية التلقائية العامة** — سطر واحد في إعدادات VS Code العامة يجعل *كل* نافذة تفتحها تُظهر اسم مجلدها في شريط العنوان. اضبطه مرة واحدة، ويعمل إلى الأبد، لأي مشروع.
- **اللون الخاص بكل مشروع** — يضع ملف `.vscode/settings.json` صغيراً في كل مشروع يحوي لوناً ورمزاً تعبيرياً مُشتقاً من اسمه. نفس المشروع له نفس اللون دوماً؛ والمشاريع المختلفة تبدو مختلفة دوماً.

يدمج مع إعداداتك الحالية (لا يحذف مفاتيحك أبداً)، وهو ثابت (يمكن تشغيله عدة مرات بنفس النتيجة)، ويتخطى المشاريع التي سبق تسميتها، ويدعم `--dry-run`.

## التثبيت

```bash
curl -fsSL -o vscode-window-labeler.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/vscode-window-labeler.tar.gz
tar xzf vscode-window-labeler.tar.gz && cd vscode-window-labeler && bash install.sh
```

## استخدامه

```bash
# Preview (writes nothing):
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects --dry-run

# Apply — point it at the folder that holds your projects:
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects
```

ثم أعد تحميل كل نافذة من نوافذ VS Code (`Ctrl/Cmd+Shift+P` → **إعادة تحميل النافذة**). هل تريد من المشاريع الجديدة أن تُلوّن نفسها تلقائياً؟ يمكن للمثبّت تفعيل مؤقت لمدة 90 ثانية — يُطبّق VS Code اللون بشكل مباشر، دون إعادة تحميل.

## أعطِه لـ Claude Code

ألصِق هذا في جلسة Claude Code مفتوحة في مجلد مشاريعك:

```
I have too many VS Code windows open and can't tell which project is which.
Set my VS Code User settings window.title to "${rootName}  ${separator}  ${activeEditorShort}"
so every window shows its folder name, and for each project folder under ~/projects add a
.vscode/settings.json with a window.title (emoji + NAME) and a workbench.colorCustomizations
titleBar color derived deterministically from the folder name. Merge, don't overwrite my
other keys, and skip projects that already have a window.title.
```

## المستودع

https://github.com/primovera12/gnesis-vault/tree/main/vscode-window-labeler
