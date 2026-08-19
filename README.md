# Switch-Scot ⚡

> **Universal High-Performance Multi-Interface Network Resilience & Load Testing Engine**  
> **محرك تقييم واختبار مرونة وأحمال الشبكات متعدد الواجهات وعابر للمنصات**  
> *Engineered for Linux (Arch, Kali, Debian, Ubuntu, Fedora) and Android (Termux with Root).*

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Android%20Termux-brightgreen.svg)]()
[![Language](https://img.shields.io/badge/Language-Arabic%20%7C%20English-orange.svg)]()

---

## 🌟 Key Features / المميزات الرئيسية

- **🌐 Dual-Language Interface (عربي / English):** واجهة تفاعلية كاملة تدعم اللغة العربية والإنجليزية باحترافية.
- **🚀 Simultaneous Multi-Interface Engine:** تشغيل وتوجيه حزم متوازية عبر كروت شبكة متعددة معاً (`1,2` أو `all`) لمضاعفة قوة التدفق.
- **🎯 Smart URL & Domain Auto-Extractor:** استخراج الـ IP والمنفذ تلقائياً من روابط صفحات الويب (مثل `http://192.168.8.1:8080/login.html`).
- **📱 True Cross-Platform:** متوافق بنسبة 100% مع أندرويد (تيرمكس عبر `tsu`) وجميع توزيعات لينكس (آرش، كالي، أوبونتو، فيدورا عبر `sudo`).
- **🛡️ 5-Layer Obfuscation Stack:** تمويه كامل (تدوير MAC، تدوير TTL عشوائياً بين 64 و 128، انتحال Hostname مخصص، مسح ذاكرة ARP، وتزوير IP الحزم `--rand-source`).
- **📊 Real-Time Live Monitor:** شاشة مراقبة لحظية مدمجة لحساب معدل الحزم في الثانية (PPS) وسرعة التدفق (Mbps).

---

## 🚀 Quick Start / التثبيت السريع

```bash
git clone https://github.com/PMoha1/Switch-Scot.git
cd Switch-Scot
chmod +x install.sh
./install.sh
```

---

## 💻 Usage / دليل التشغيل

### 1. القائمة التفاعلية السهلة (Interactive Easy-Menu):
فقط اكتب الأمر التالي وستفتح لك القائمة التفاعلية باللغة العربية:
```bash
sudo switch-scot
```

```text
  ___         _ _       _          ___ cot ⚡
 / __|_ __ __(_) |_ ___| |_ _____ / __| __ ___ 
 \__ \ V  V /| |  _/ __| ' \_____\__ \ _| '_ \
 |___/\_/\_/ |_|\__\___|_||_|    |___/__| .__/
                                         |_|   
 Universal Multi-Interface Network Resilience Engine v3.5 [AR/EN]

=================================================================
 [1] 🇾🇪 العربية (Arabic)
 [2] 🏴‍☠️ English
=================================================================
[؟/Query] Select Language / اختر اللغة [1-2, default 1]: 1

=================================================================
 🛠️  لوحة التحكم والإعداد التفاعلي السريع (Switch-Scot)
=================================================================

[+] كروت الشبكة المكتشفة في النظام:
  [1] wlp4s0 (الافتراضي)
  [2] wlp9s0f4u2
  [3] enp3s0
  [A] تشغيل جميع الكروت معاً في نفس اللحظة (وضع التيربو الخارق 🚀)

[؟] اختر كرت الشبكة [مثال: 1 أو 1,2 أو A للكل - الافتراضي 1]: 1,2
 -> تم تحديد الكروت: wlp4s0, wlp9s0f4u2

[؟] أدخل عنوان الهدف (IP أو رابط صفحة الويب) [الافتراضي: 192.168.8.1]: 
 -> عنوان الهدف المعتمد (Host/IP): 192.168.8.1

[؟] أدخل رقم المنفذ المستهدف [الافتراضي: 80]: 80
 -> المنفذ النهائي: 80

[+] أوضاع الفحص والتقييم:
  [1] 1. TCP-SYN  - استنزاف طابور الاتصالات في النواة (الافتراضي / الأقوى)
  [2] 2. UDP      - ضغط واختبار ذاكرة التخزين المؤقتة (Buffer Stress)
  [3] 3. ICMP     - قياس استجابة وتأخير معالج الراوتر (Control Plane)
  [4] 4. TCP-ACK  - اختبار فلاتر جدران الحماية المتقدمة (Stateful Firewall)

[؟] اختر وضع الفحص [1-4، الافتراضي 1]: 1
 -> الوضع المعتمد: TCP-SYN

[؟] أدخل اسم الجهاز المخصص ليظهر في الراوتر [الافتراضي: جهاز ذكي عشوائي]: Moha-Device
 -> اسم الجهاز المنحول: Moha-Device

[+] سياسة تمويه وتدوير الماك أدرس (MAC Address):
  [1] 1. الاحتفاظ بالماك الحالي (موصى به للواي فاي النشط على اللابتوب)
  [2] 2. تدوير الماك بالكامل عشوائياً (تمويه فيزيائي شامل لكرت الشبكة)

[؟] اختر سياسة الماك [1-2، الافتراضي 1]: 1
 -> سياسة الماك: الاحتفاظ بالماك الحالي لضمان استقرار الواي فاي

-----------------------------------------------------------------
⚡ اضغط [ENTER] لإطلاق محرك Switch-Scot والبدء فوراً...
```

---

### 2. وضع سطر الأوامر المباشر (CLI Fast Mode):
```bash
# تشغيل مباشر مع رابط صفحة ويب وحفظ الماك:
sudo switch-scot -t "http://192.168.8.1:8080/login.html" --no-mac

# تشغيل كرتين معاً بالتوازي مع تحديد اسم جهاز مخصص:
sudo switch-scot -i wlp4s0 wlp9s0f4u2 -t 192.168.8.1 -p 80 -H "Smart-TV" --no-mac

# تشغيل شاشة المراقبة اللحظية:
switch-scot-monitor
```

---

## ⚠️ Disclaimer / إخلاء مسؤولية

This tool is strictly developed for educational purposes, authorized security assessments, and network resilience testing. Usage against unauthorized targets without explicit prior consent is strictly prohibited. The author assumes no liability for misuse.  
تم تطوير هذه الأداة حصرياً للأغراض التعليمية واختبار مرونة وقدرة الشبكات المصرح بفحصها. يُحظر استخدامها ضد أي أهداف غير مصرح بها.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
