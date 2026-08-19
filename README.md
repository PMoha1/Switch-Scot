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
   _____         _ _       _         ____             _   
  / ____|       (_) |     | |       / ____|          | |  
 | (_____      ___| |_ ___| |__ ___| (___   ___  ___ | |_ 
  \___ \ \ /\ / / | __/ __| '_ \_____\___ \ / __|/ _ \| __|
  ____) \ V  V /| | || (__| | | |    ____) | (__| (_) | |_ 
 |_____/ \_/\_/ |_|\__\___|_| |_|   |_____/ \___|\___/ \__|
                                                           ⚡ v3.6
 🇾🇪 المطور : محمد يقين مجمل الفايق | صنعاء - اليمن
 🇾🇪 Author : Mohammed Yaqeen | Sana'a - Yemen

=================================================================
 1. 🇾🇪 اللغة العربية (Arabic)
 2. 🏴‍☠️ English
=================================================================
>> Select Language / اختر اللغة [Default 1]: 1

=== لوحة التحكم والتشغيل التفاعلي السريع ===
-----------------------------------------------------------------

* كروت الشبكة المكتشفة في جهازك:
  1. wlp4s0 (الافتراضي)
  2. wlp9s0f4u2
  3. enp3s0
  A. تشغيل كل الكروت معاً في نفس الوقت (وضع التيربو الخارق)

>> رقم الكرت المطلوب [الافتراضي 1]: 1,2
* الكروت المختارة: wlp4s0, wlp9s0f4u2

>> عنوان الهدف أو الرابط [الافتراضي 192.168.8.1]: http://192.168.8.1:8080/login.html
* عنوان الهدف: 192.168.8.1
* المنفذ المستخرج تلقائياً: 8080

>> رقم المنفذ المطلوب [الافتراضي 8080]: 8080
* المنفذ النهائي: 8080

* أوضاع الفحص والتقييم المتاحة:
  1. TCP-SYN (استنزاف طابور اتصالات الراوتر - الأقوى)
  2. UDP (ضغط الذاكرة المؤقتة للراوتر)
  3. ICMP (قياس سرعة استجابة وتأخير المعالج)
  4. TCP-ACK (فحص واختبار جدار الحماية)

>> رقم وضع الفحص [الافتراضي 1]: 1
* الوضع المعتمد: TCP-SYN

>> اسم الجهاز المنحول ليظهر في الراوتر [اضغط Enter للاسم العشوائي]: Moha-Device
* اسم الجهاز المعتمد: Moha-Device

* خيارات الماك أدرس (MAC Address):
  1. الإبقاء على الماك الحالي (موصى به لثبات الواي فاي)
  2. تدوير الماك عشوائياً (تمويه فيزيائي شامل)

>> خيار الماك [الافتراضي 1]: 1
* سياسة الماك: الحفاظ على الماك الحالي لثبات الاتصال

=================================================================
>> اضغط ENTER للبدء والانطلاق فوراً...
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

## 👨‍💻 About the Developer / نبذة عن المطور

### 🇾🇪 **محمد يقين مجمل الفايق (Mohammed Yaqeen Mujamal Al-Faiq)**
- 📍 **الموقع (Location):** الجمهورية اليمنية - صنعاء (Yemen - Sana'a)
- 📺 **صانع محتوى تقني (Tech Creator):** صاحب قناة يوتيوب مخصصة لتقديم شروحات متقدمة وتجارب عملية في أنظمة وتوزيعات لينكس المختلفة (Arch, Kali, Debian, Ubuntu).
- 💡 **الاهتمامات والخبرات (Interests & Focus):**
  - اختبار وتطوير أدوات الشبكات والأمن السيبراني وتقييم المرونة.
  - التجارب العميقة على توزيعات لينكس وإدارة الأنظمة المتقدمة.
  - أبحاث وتطبيقات الذكاء الاصطناعي والموديلات المحلية غير المقيدة (Local & Uncensored AI Models).

---

## ⚠️ Disclaimer / إخلاء مسؤولية

This tool is strictly developed for educational purposes, authorized security assessments, and network resilience testing. Usage against unauthorized targets without explicit prior consent is strictly prohibited. The author assumes no liability for misuse.  
تم تطوير هذه الأداة حصرياً للأغراض التعليمية واختبار مرونة وقدرة الشبكات المصرح بفحصها. يُحظر استخدامها ضد أي أهداف غير مصرح بها.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
