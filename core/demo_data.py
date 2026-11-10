"""Демо-контент сайта на трёх языках (ru / kk / en).

Цены — ориентировочные оценки по рынку Алматы, кейсы — вымышленные (is_demo=True).
Всё это редактируется в CRM и должно быть заменено реальными данными до запуска рекламы.
Казахские тексты стоит вычитать носителю языка.
"""


def T(ru: str, kk: str, en: str) -> dict:
    return {"ru": ru, "kk": kk, "en": en}


SERVICES = [
    {
        "slug": "ajax",
        "icon": "hub",
        "order": 1,
        "price_from": 100000,
        "title": T("Сигнализация Ajax, RAPTOR, STEMAX, Dahua и другие", "Ajax, RAPTOR, STEMAX, Dahua және басқа дабылдар", "Ajax, RAPTOR, STEMAX, Dahua and other alarm systems"),
        "h1": T("Установка сигнализации Ajax, RAPTOR, STEMAX, Dahua в Казахстане", "Қазақстанда Ajax, RAPTOR, STEMAX, Dahua дабылдарын орнату", "Ajax, RAPTOR, STEMAX and Dahua alarm installation in Kazakhstan"),
        "offer": T(
            "Беспроводная охранная система с управлением со смартфона. Монтаж квартиры — за 1 день, без штробления стен.",
            "Смартфоннан басқарылатын сымсыз күзет жүйесі. Пәтерге монтаж — 1 күнде, қабырғаны ойып-бұзусыз.",
            "A wireless security system controlled from your smartphone. An apartment is installed in one day, with no wall chasing.",
        ),
        "summary": T(
            "Беспроводные датчики движения, открытия, дыма и протечки. Тревоги и управление — в приложении.",
            "Қозғалыс, ашылу, түтін және су ағу сымсыз датчиктері. Дабылдар мен басқару — қосымшада.",
            "Wireless motion, door, smoke and leak sensors. Alerts and control in a mobile app.",
        ),
        "intro": T(
            "Ajax — беспроводная охранная система: хаб, датчики и сирены связываются по защищённому радиоканалу, поэтому монтаж проходит без прокладки кабелей и ремонта.\n\n"
            "Мы приезжаем на объект, определяем уязвимые места, подбираем комплект и устанавливаем его. Настраиваем сценарии (например, «Ушёл из дома» одной кнопкой), подключаем приложение для всей семьи, организуем подключение к пульту централизованного наблюдения (ПЦН) КУЗЕТ для реагирования мобильной группы по договору и берем систему на регулярное техническое обслуживание.",
            "Ajax — сымсыз күзет жүйесі: хаб, датчиктер мен сиреналар қорғалған радиоарна арқылы байланысады, сондықтан монтаж кабель тартусыз және жөндеусіз өтеді.\n\n"
            "Біз нысанға келіп, осал жерлерді анықтаймыз, жиынтықты таңдап, орнатамыз. Сценарийлерді баптаймыз (мысалы, бір батырмамен «Үйден шықтым»), бүкіл отбасына қосымшаны қосамыз, шарт бойынша жедел топтың әрекет етуі үшін КҮЗЕТ орталықтандырылған пультіне қосылуды ұйымдастырамыз және жүйені тұрақты техникалық қызметке аламыз.",
            "Ajax is a wireless security system: the hub, sensors and sirens communicate over an encrypted radio channel, so installation needs no cabling or renovation.\n\n"
            "We visit the site, identify weak points, select a kit and install it. We set up automated scenarios, connect the mobile app, organise connection to the KUZET (Security) central monitoring station for mobile group response under contract, and provide ongoing technical maintenance.",
        ),
        "benefits": T(
            "Монтаж без штробления и пыли\nУправление и тревоги в приложении\nРаботает при отключении света и интернета\nПодключение к пультовой охране КУЗЕТ\nОрганизация выезда мобильной группы по договору\nРегулярное техническое обслуживание",
            "Қабырғаны ойып-бұзусыз және шаңсыз монтаж\nҚосымшада басқару және дабылдар\nЖарық пен интернет өшсе де жұмыс істейді\nКҮЗЕТ пульттік күзетіне қосылу\nШарт бойынша жедел топтың шығуын ұйымдастыру\nТұрақты техникалық қызмет көрсету",
            "No wall chasing, no dust\nControl and alerts in the app\nKeeps working during power and internet outages\nConnection to KUZET (Security) central monitoring\nMobile response team dispatched under contract\nOngoing preventative maintenance",
        ),
        "object_types": T(
            "Квартира\nЧастный дом\nОфис\nМагазин\nДача",
            "Пәтер\nЖеке үй\nКеңсе\nДүкен\nСаяжай",
            "Apartment\nHouse\nOffice\nShop\nCountry house",
        ),
        "seo_title": T(
            "Установка сигнализации Ajax, RAPTOR, STEMAX, Dahua в Казахстане — цены под ключ",
            "Қазақстанда Ajax, RAPTOR, STEMAX, Dahua дабылдарын орнату — толық баға",
            "Ajax, RAPTOR, STEMAX, Dahua Alarm Installation in Kazakhstan — Turnkey Prices",
        ),
        "seo_description": T(
            "Монтаж сигнализации Ajax, RAPTOR, STEMAX, Dahua в квартире, доме или офисе в Казахстане. Комплекты от 100 000 ₸ с установкой, бесплатный выезд и смета.",
            "Қазақстандағы пәтерге, үйге немесе кеңсеге Ajax, RAPTOR, STEMAX, Dahua дабылдарын орнату. Орнатумен бірге жиынтықтар 100 000 ₸-ден, тегін шығу және смета.",
            "Ajax, RAPTOR, STEMAX and Dahua alarm installation for apartments, houses and offices in Kazakhstan. Kits with installation from 100,000 ₸, free site visit and estimate.",
        ),
        "packages": [
            {
                "price_from": 100000,
                "is_popular": True,
                "name": T("Квартира", "Пәтер", "Apartment"),
                "items": T(
                    "Хаб Hub 2\n2 датчика движения\n2 датчика открытия\nКлавиатура\nСирена\nМонтаж и настройка приложения",
                    "Hub 2 хабы\n2 қозғалыс датчигі\n2 ашылу датчигі\nПернетақта\nСирена\nМонтаж және қосымшаны баптау",
                    "Hub 2\n2 motion detectors\n2 door/window sensors\nKeypad\nSiren\nInstallation and app setup",
                ),
            },
            {
                "price_from": 450000,
                "name": T("Офис / магазин", "Кеңсе / дүкен", "Office / shop"),
                "items": T(
                    "Hub 2 Plus\n4 датчика движения\n3 датчика открытия\nТревожная кнопка\nСирена\nМонтаж и настройка",
                    "Hub 2 Plus\n4 қозғалыс датчигі\n3 ашылу датчигі\nДабыл түймесі\nСирена\nМонтаж және баптау",
                    "Hub 2 Plus\n4 motion detectors\n3 door/window sensors\nPanic button\nSiren\nInstallation and setup",
                ),
            },
            {
                "price_from": 650000,
                "name": T("Дом", "Үй", "House"),
                "items": T(
                    "Hub 2 Plus\n6 датчиков движения (2 уличных)\n5 датчиков открытия\nДатчики дыма и протечки\nУличная сирена\nМонтаж и настройка",
                    "Hub 2 Plus\n6 қозғалыс датчигі (2 сыртқы)\n5 ашылу датчигі\nТүтін және су ағу датчиктері\nСыртқы сирена\nМонтаж және баптау",
                    "Hub 2 Plus\n6 motion detectors (2 outdoor)\n5 door/window sensors\nSmoke and leak detectors\nOutdoor siren\nInstallation and setup",
                ),
            },
        ],
        "faqs": [
            (
                T("Нужно ли сверлить стены и прокладывать провода?", "Қабырғаны тесіп, сым тарту керек пе?", "Do you need to drill walls and run cables?"),
                T(
                    "Нет. Ajax полностью беспроводной: датчики крепятся на кронштейны, монтаж квартиры обычно занимает один день.",
                    "Жоқ. Ajax толығымен сымсыз: датчиктер кронштейнге бекітіледі, пәтерге монтаж әдетте бір күн алады.",
                    "No. Ajax is fully wireless: sensors mount on brackets, and an apartment is usually done in one day.",
                ),
            ),
            (
                T("Что будет, если отключат свет или интернет?", "Жарық не интернет өшсе не болады?", "What if the power or internet goes out?"),
                T(
                    "Хаб работает от встроенного аккумулятора и переключается на мобильную связь по SIM-карте, так что тревоги продолжат приходить.",
                    "Хаб кіріктірілген аккумулятормен жұмыс істейді және SIM-карта арқылы ұялы байланысқа ауысады, сондықтан дабылдар келе береді.",
                    "The hub runs on its built-in battery and switches to mobile data via a SIM card, so alerts keep coming.",
                ),
            ),
            (
                T("Есть ли абонентская плата?", "Абоненттік төлем бар ма?", "Is there a monthly fee?"),
                T(
                    "За приложение Ajax платить не нужно. Абонплата появится, только если вы захотите подключить пульт охранной компании, — поможем выбрать.",
                    "Ajax қосымшасы үшін төлеудің қажеті жоқ. Абоненттік төлем күзет компаниясының пультін қосқыңыз келгенде ғана пайда болады — таңдауға көмектесеміз.",
                    "The Ajax app is free. A monthly fee applies only if you connect a security company's monitoring — we'll help you choose.",
                ),
            ),
        ],
    },
    {
        "slug": "videonablyudenie",
        "icon": "camera",
        "order": 2,
        "price_from": 80000,
        "title": T("Видеонаблюдение", "Бейнебақылау", "Video surveillance"),
        "h1": T("Установка видеонаблюдения в Казахстане под ключ", "Қазақстанда бейнебақылауды толық орнату", "Turnkey CCTV installation in Kazakhstan"),
        "offer": T(
            "IP-камеры 4 Мп с записью в архив и просмотром со смартфона. Подберём камеры под каждую зону и смонтируем за 1–2 дня.",
            "Мұрағатқа жазатын және смартфоннан көруге болатын 4 Мп IP-камералар. Әр аймаққа камера таңдап, 1–2 күнде орнатамыз.",
            "4 MP IP cameras with recording and smartphone viewing. We pick a camera for every zone and install in 1–2 days.",
        ),
        "summary": T(
            "Внутренние и уличные IP-камеры, регистратор с архивом, онлайн-просмотр с телефона.",
            "Ішкі және сыртқы IP-камералар, мұрағаты бар тіркеуіш, телефоннан онлайн көру.",
            "Indoor and outdoor IP cameras, a recorder with archive, live view from your phone.",
        ),
        "intro": T(
            "Начинаем с выезда: смотрим, какие зоны важно контролировать, где нужна ночная съёмка и распознавание номеров или лиц. Затем подбираем камеры, регистратор и объём диска под нужную глубину архива.\n\n"
            "Монтируем аккуратно: кабель в гофре или кабель-канале, камеры на высоте, недоступной для вандалов. В конце настраиваем просмотр на всех телефонах владельца и показываем, как найти запись по времени.",
            "Нысанға барудан бастаймыз: қай аймақтарды бақылау маңызды, қай жерде түнгі түсірілім және нөмірлер мен беттерді тану қажет екенін қараймыз. Содан кейін мұрағаттың қажетті тереңдігіне қарай камераларды, тіркеуішті және диск көлемін таңдаймыз.\n\n"
            "Мұқият орнатамыз: кабель гофрада немесе кабель-арнада, камералар бұзақылар жете алмайтын биіктікте. Соңында иесінің барлық телефондарында көруді баптап, жазбаны уақыт бойынша қалай табуға болатынын көрсетеміз.",
            "We start with a site visit: which zones matter, where night vision and licence-plate or face recognition are needed. Then we select cameras, a recorder and disk size for the archive depth you need.\n\n"
            "Installation is neat: cables in conduit or trunking, cameras mounted out of vandals' reach. Finally we set up viewing on every owner's phone and show how to find a recording by time.",
        ),
        "benefits": T(
            "Чёткая картинка днём и ночью\nПросмотр и архив в телефоне\nУличные камеры с защитой от пыли и влаги\nУведомления о движении в нужных зонах\nВозможна связка с сигнализацией AJAX\nОбслуживание и расширение системы",
            "Күндіз де, түнде де анық сурет\nТелефонда көру және мұрағат\nШаң мен ылғалдан қорғалған сыртқы камералар\nҚажетті аймақтардағы қозғалыс туралы хабарламалар\nAJAX дабылымен біріктіруге болады\nЖүйеге қызмет көрсету және кеңейту",
            "Sharp image day and night\nLive view and archive on your phone\nWeather-proof outdoor cameras\nMotion alerts for selected zones\nCan be linked with an AJAX alarm\nMaintenance and expansion",
        ),
        "object_types": T(
            "Частный дом\nМагазин\nКафе и ресторан\nОфис\nСклад\nПодъезд и паркинг",
            "Жеке үй\nДүкен\nКафе және мейрамхана\nКеңсе\nҚойма\nКіреберіс және паркинг",
            "House\nShop\nCafé and restaurant\nOffice\nWarehouse\nEntrance and parking",
        ),
        "seo_title": T(
            "Установка видеонаблюдения в Казахстане — цены на камеры под ключ",
            "Қазақстанда бейнебақылау орнату — камералардың толық бағасы",
            "CCTV Installation in Kazakhstan — Turnkey Camera Prices",
        ),
        "seo_description": T(
            "Монтаж IP-камер видеонаблюдения для дома, магазина и офиса в Казахстане. Видеонаблюдение под ключ от 80 000 ₸, просмотр с телефона.",
            "Қазақстанда үйге, дүкенге және кеңсеге бейнебақылау IP-камераларын орнату. Толық бейнебақылау 80 000 ₸-ден, телефоннан көру.",
            "IP CCTV installation for homes, shops and offices in Kazakhstan. Turnkey CCTV from 80,000 ₸, viewing from your phone.",
        ),
        "packages": [
            {
                "price_from": 80000,
                "is_popular": True,
                "name": T("4 камеры", "4 камера", "4 cameras"),
                "items": T(
                    "4 IP-камеры 4 Мп\nРегистратор\nЖёсткий диск 1 ТБ\nПросмотр с телефона\nМонтаж и настройка",
                    "4 Мп 4 IP-камера\nТіркеуіш\n1 ТБ қатқыл диск\nТелефоннан көру\nМонтаж және баптау",
                    "4 × 4 MP IP cameras\nRecorder\n1 TB hard drive\nPhone viewing\nInstallation and setup",
                ),
            },
            {
                "price_from": 420000,
                "name": T("8 камер", "8 камера", "8 cameras"),
                "items": T(
                    "8 IP-камер 4 Мп\nРегистратор\nЖёсткий диск 2 ТБ\nPoE-коммутатор\nМонтаж и настройка",
                    "4 Мп 8 IP-камера\nТіркеуіш\n2 ТБ қатқыл диск\nPoE-коммутатор\nМонтаж және баптау",
                    "8 × 4 MP IP cameras\nRecorder\n2 TB hard drive\nPoE switch\nInstallation and setup",
                ),
            },
            {
                "price_from": 850000,
                "name": T("16 камер", "16 камера", "16 cameras"),
                "items": T(
                    "16 IP-камер\nРегистратор\nЖёсткий диск 4 ТБ\nШкаф и ИБП\nМонтаж и настройка",
                    "16 IP-камера\nТіркеуіш\n4 ТБ қатқыл диск\nШкаф және ҮҚК\nМонтаж және баптау",
                    "16 IP cameras\nRecorder\n4 TB hard drive\nRack and UPS\nInstallation and setup",
                ),
            },
        ],
        "faqs": [
            (
                T("Сколько дней хранится архив?", "Мұрағат неше күн сақталады?", "How long is footage stored?"),
                T(
                    "Зависит от числа камер и объёма диска. Для 4 камер и диска 1 ТБ — около 10 дней непрерывной записи, при записи по движению — дольше. Подберём диск под нужный срок.",
                    "Камералар саны мен диск көлеміне байланысты. 4 камера мен 1 ТБ диск үшін — шамамен 10 күн үздіксіз жазба, қозғалыс бойынша жазғанда — ұзағырақ. Дискті қажетті мерзімге қарай таңдаймыз.",
                    "It depends on the number of cameras and disk size. For 4 cameras and a 1 TB disk it is about 10 days of continuous recording, longer with motion-only recording. We size the disk for the period you need.",
                ),
            ),
            (
                T("Можно смотреть камеры с телефона?", "Камераларды телефоннан көруге бола ма?", "Can I watch the cameras on my phone?"),
                T(
                    "Да, настраиваем бесплатное приложение производителя: онлайн-просмотр, архив и уведомления о движении.",
                    "Иә, өндірушінің тегін қосымшасын баптаймыз: онлайн көру, мұрағат және қозғалыс туралы хабарламалар.",
                    "Yes, we set up the manufacturer's free app: live view, archive and motion alerts.",
                ),
            ),
            (
                T("Можно ли ставить камеры в подъезде или на фасаде?", "Камераларды кіреберіске не қасбетке қоюға бола ма?", "Can cameras be installed in the stairwell or on the facade?"),
                T(
                    "Можно, но нужно соблюдать правила размещения и получить согласие соседей или ОСИ. Подскажем, как это оформить.",
                    "Болады, бірақ орналастыру ережелерін сақтап, көршілердің немесе ПИБ-тің келісімін алу керек. Қалай рәсімдеуге болатынын айтып береміз.",
                    "Yes, but placement rules and the consent of neighbours or the condominium association apply. We'll explain the paperwork.",
                ),
            ),
        ],
    },
    {
        "slug": "skud",
        "icon": "access",
        "order": 3,
        "price_from": 300000,
        "title": T("СКУД", "Кіруді бақылау (СКУД)", "Access control"),
        "h1": T(
            "Установка СКУД в Казахстане — контроль доступа и учёт времени",
            "Қазақстанда кіруді бақылау жүйесін (СКУД) орнату",
            "Access control installation in Kazakhstan",
        ),
        "offer": T(
            "Доступ по картам, отпечатку или лицу, учёт рабочего времени и журнал проходов. От одной двери до бизнес-центра.",
            "Карта, саусақ ізі немесе бет арқылы кіру, жұмыс уақытын есепке алу және өту журналы. Бір есіктен бизнес-орталыққа дейін.",
            "Entry by card, fingerprint or face, time tracking and an access log. From a single door to a business centre.",
        ),
        "summary": T(
            "Электронные замки, считыватели карт и Face ID, турникеты и учёт рабочего времени.",
            "Электрондық құлыптар, карта оқығыштар мен Face ID, турникеттер және жұмыс уақытын есепке алу.",
            "Electronic locks, card and Face ID readers, turnstiles and time tracking.",
        ),
        "intro": T(
            "Система контроля доступа решает две задачи: пускает только тех, кому разрешено, и записывает, кто и когда прошёл. Это заменяет ключи, которые теряют и копируют, и даёт честный учёт рабочего времени.\n\n"
            "Мы проектируем схему точек доступа, подбираем контроллеры, считыватели и замки, прокладываем кабель и настраиваем программу. Сотрудников и права доступа можно менять за минуту — без замены замков.",
            "Кіруді бақылау жүйесі екі міндетті шешеді: тек рұқсаты барларды кіргізеді және кім, қашан өткенін жазып отырады. Бұл жоғалатын және көшірілетін кілттерді алмастырып, жұмыс уақытын әділ есепке алуға мүмкіндік береді.\n\n"
            "Біз кіру нүктелерінің сызбасын жобалаймыз, контроллерлерді, оқығыштар мен құлыптарды таңдаймыз, кабель тартып, бағдарламаны баптаймыз. Қызметкерлер мен кіру құқықтарын бір минутта өзгертуге болады — құлыптарды ауыстырусыз.",
            "An access control system does two things: it lets in only authorised people and records who passed and when. It replaces keys that get lost or copied and gives you fair time tracking.\n\n"
            "We design the access-point layout, choose controllers, readers and locks, run the cabling and configure the software. Staff and permissions can be changed in a minute — no lock replacement needed.",
        ),
        "benefits": T(
            "Доступ по карте, коду, отпечатку или лицу\nЖурнал проходов и учёт рабочего времени\nУдалённое открытие двери\nСвязка с видеонаблюдением\nАварийная разблокировка при пожаре\nМасштабирование на новые двери",
            "Карта, код, саусақ ізі немесе бет арқылы кіру\nӨту журналы және жұмыс уақытын есепке алу\nЕсікті қашықтан ашу\nБейнебақылаумен біріктіру\nӨрт кезінде апаттық құлыпты ашу\nЖаңа есіктерге кеңейту",
            "Entry by card, PIN, fingerprint or face\nAccess log and time tracking\nRemote door opening\nLinked with CCTV\nEmergency unlock in case of fire\nEasy to add more doors",
        ),
        "object_types": T(
            "Офис\nБизнес-центр\nПроизводство\nСклад\nЖилой комплекс\nФитнес-клуб",
            "Кеңсе\nБизнес-орталық\nӨндіріс\nҚойма\nТұрғын үй кешені\nФитнес-клуб",
            "Office\nBusiness centre\nFactory\nWarehouse\nResidential complex\nFitness club",
        ),
        "seo_title": T(
            "Установка СКУД в Казахстане — системы контроля доступа под ключ",
            "Қазақстанда СКУД орнату — кіруді бақылау жүйелері",
            "Access Control Installation in Kazakhstan — Turnkey Systems",
        ),
        "seo_description": T(
            "Монтаж СКУД в Казахстане: электронные замки, карты, Face ID, турникеты и учёт рабочего времени. Одна дверь под ключ — от 300 000 ₸.",
            "Қазақстанда СКУД монтажы: электрондық құлыптар, карталар, Face ID, турникеттер және жұмыс уақытын есепке алу. Бір есік — 300 000 ₸-ден.",
            "Access control in Kazakhstan: electronic locks, cards, Face ID, turnstiles and time tracking. One door, turnkey, from 300,000 ₸.",
        ),
        "packages": [
            {
                "price_from": 300000,
                "is_popular": True,
                "name": T("1 дверь", "1 есік", "1 door"),
                "items": T(
                    "Контроллер\nСчитыватель карт\nЭлектромагнитный замок\nКнопка выхода\n10 карт доступа\nМонтаж и настройка",
                    "Контроллер\nКарта оқығыш\nЭлектромагниттік құлып\nШығу түймесі\n10 кіру картасы\nМонтаж және баптау",
                    "Controller\nCard reader\nMagnetic lock\nExit button\n10 access cards\nInstallation and setup",
                ),
            },
            {
                "price_from": 450000,
                "name": T("Офис на 4 двери", "4 есікті кеңсе", "Office, 4 doors"),
                "items": T(
                    "Сетевые контроллеры\n4 считывателя\nЗамки и доводчики\nУчёт рабочего времени\nПрограмма и обучение",
                    "Желілік контроллерлер\n4 оқығыш\nҚұлыптар мен жапқыштар\nЖұмыс уақытын есепке алу\nБағдарлама және оқыту",
                    "Network controllers\n4 readers\nLocks and door closers\nTime tracking\nSoftware and training",
                ),
            },
            {
                "price_from": 1200000,
                "name": T("Турникет + Face ID", "Турникет + Face ID", "Turnstile + Face ID"),
                "items": T(
                    "Турникет\nТерминал распознавания лиц\nКонтроллер\nМонтаж и настройка",
                    "Турникет\nБетті тану терминалы\nКонтроллер\nМонтаж және баптау",
                    "Turnstile\nFace recognition terminal\nController\nInstallation and setup",
                ),
            },
        ],
        "faqs": [
            (
                T("Что будет с дверью, если отключат электричество?", "Электр өшсе есікке не болады?", "What happens to the door during a power cut?"),
                T(
                    "Ставим блок бесперебойного питания. При пожарной тревоге и полном обесточивании электромагнитные замки открываются — так требуют нормы безопасности.",
                    "Үздіксіз қуат блогын орнатамыз. Өрт дабылы кезінде және толық қуатсыз қалғанда электромагниттік құлыптар ашылады — қауіпсіздік нормалары соны талап етеді.",
                    "We install a UPS. In a fire alarm or full power loss, magnetic locks release — safety regulations require it.",
                ),
            ),
            (
                T("Можно ли использовать существующие пропуска?", "Бұрыннан бар рұқсатнамаларды қолдануға бола ма?", "Can we use our existing badges?"),
                T(
                    "Часто да: большинство систем читает карты EM-Marine и Mifare. Проверим ваши карты на выезде.",
                    "Көбіне иә: жүйелердің көбі EM-Marine және Mifare карталарын оқиды. Карталарыңызды барған кезде тексереміз.",
                    "Often yes: most systems read EM-Marine and Mifare cards. We'll check your cards on site.",
                ),
            ),
        ],
    },
    {
        "slug": "slabotochnye-sistemy",
        "icon": "network",
        "order": 4,
        "price_from": 100000,
        "title": T("Слаботочные системы", "Әлсіз ток жүйелері", "Low-voltage systems"),
        "h1": T("Монтаж слаботочных систем и ЛВС в Казахстане", "Қазақстанда әлсіз ток жүйелері мен ЖЕЖ монтажы", "Low-voltage and LAN installation in Kazakhstan"),
        "offer": T(
            "Локальные сети, Wi-Fi, телефония, домофоны и кабельные трассы. Проектируем, монтируем и сдаём с тестированием каждой линии.",
            "Жергілікті желілер, Wi-Fi, телефония, домофондар және кабель трассалары. Жобалаймыз, орнатамыз және әр желіні тестілеп тапсырамыз.",
            "LAN, Wi-Fi, telephony, intercoms and cable routes. We design, install and hand over with every line tested.",
        ),
        "summary": T(
            "Структурированные кабельные сети, Wi-Fi, телефония и домофоны для офисов и домов.",
            "Кеңселер мен үйлерге арналған құрылымдалған кабель желілері, Wi-Fi, телефония және домофондар.",
            "Structured cabling, Wi-Fi, telephony and intercoms for offices and homes.",
        ),
        "intro": T(
            "Слаботочные системы — это «нервная система» здания: интернет, Wi-Fi, камеры, СКУД и домофоны работают по одним кабельным трассам. Если их спроектировать заранее, потом не придётся вскрывать стены.\n\n"
            "Мы делаем проект, прокладываем кабель, собираем коммутационный шкаф, маркируем и тестируем каждую линию, а в конце отдаём схему сети.",
            "Әлсіз ток жүйелері — ғимараттың «жүйке жүйесі»: интернет, Wi-Fi, камералар, СКУД және домофондар бір кабель трассалары арқылы жұмыс істейді. Оларды алдын ала жобаласаңыз, кейін қабырғаны ашудың қажеті болмайды.\n\n"
            "Біз жоба жасаймыз, кабель тартамыз, коммутациялық шкафты жинаймыз, әр желіні таңбалап, тестілейміз, соңында желі сызбасын береміз.",
            "Low-voltage systems are the building's nervous system: internet, Wi-Fi, cameras, access control and intercoms run over the same cable routes. Plan them in advance and you won't have to open walls later.\n\n"
            "We design the network, pull the cable, assemble the network rack, label and test every line, and hand over a network diagram at the end.",
        ),
        "benefits": T(
            "Проект и смета до начала работ\nМаркировка и тестирование каждой линии\nСборка коммутационного шкафа\nWi-Fi без мёртвых зон\nСхема сети при сдаче\nГотовность под камеры и СКУД",
            "Жұмыс басталғанға дейін жоба және смета\nӘр желіні таңбалау және тестілеу\nКоммутациялық шкафты жинау\nӨлі аймақтарсыз Wi-Fi\nТапсыру кезінде желі сызбасы\nКамералар мен СКУД-қа дайындық",
            "Design and estimate before work starts\nEvery line labelled and tested\nNetwork rack assembly\nWi-Fi without dead zones\nNetwork diagram on handover\nReady for cameras and access control",
        ),
        "object_types": T(
            "Офис\nЧастный дом\nМагазин\nСклад\nРесторан",
            "Кеңсе\nЖеке үй\nДүкен\nҚойма\nМейрамхана",
            "Office\nHouse\nShop\nWarehouse\nRestaurant",
        ),
        "seo_title": T(
            "Монтаж слаботочных систем в Казахстане — ЛВС, Wi-Fi, СКС",
            "Қазақстанда әлсіз ток жүйелерін орнату — ЖЕЖ, Wi-Fi",
            "Low-Voltage Installation in Kazakhstan — LAN, Wi-Fi, Cabling",
        ),
        "seo_description": T(
            "Проектирование и монтаж локальных сетей, Wi-Fi, телефонии и домофонов в Казахстане. Монтаж под ключ — от 100 000 ₸.",
            "Қазақстанда жергілікті желілерді, Wi-Fi, телефония мен домофондарды жобалау және орнату. Толық монтаж — 100 000 ₸-ден.",
            "Design and installation of LAN, Wi-Fi, telephony and intercoms in Kazakhstan. Turnkey installation from 100,000 ₸.",
        ),
        "packages": [
            {
                "price_from": 100000,
                "is_popular": True,
                "name": T("Небольшая сеть", "Шағын желі", "Small network"),
                "items": T(
                    "Кабельные линии\nРозетки RJ-45\nКроссировка в шкафу\nТестирование линий",
                    "Кабель желілері\nRJ-45 розеткалары\nШкафта кросстау\nЖелілерді тестілеу",
                    "Cable lines\nRJ-45 sockets\nPatching in the rack\nLine testing",
                ),
            },
            {
                "price_from": None,
                "name": T("Офис под ключ", "Кеңсе толығымен", "Turnkey office"),
                "price_note": T("по замеру", "өлшеу бойынша", "after site survey"),
                "items": T(
                    "Проект сети\nЛВС и коммутационный шкаф\nWi-Fi\nIP-телефония\nСхема сети",
                    "Желі жобасы\nЖЕЖ және коммутациялық шкаф\nWi-Fi\nIP-телефония\nЖелі сызбасы",
                    "Network design\nLAN and network rack\nWi-Fi\nIP telephony\nNetwork diagram",
                ),
            },
        ],
        "faqs": [
            (
                T("Сколько стоит монтаж сети в офисе?", "Кеңседе желі орнату қанша тұрады?", "How much does office cabling cost?"),
                T(
                    "Считаем по числу точек и длине трасс. Ориентир — от 100 000 ₸ за монтаж под ключ; точную смету дадим после бесплатного замера.",
                    "Нүктелер саны мен трасса ұзындығына қарай есептейміз. Бағдар — толық монтаж 100 000 ₸-ден; нақты сметаны тегін өлшеуден кейін береміз.",
                    "We price by the number of points and route length. Guide price: from 100,000 ₸ for turnkey installation; exact estimate after a free survey.",
                ),
            ),
        ],
    },
]

GENERAL_FAQS = [
    (
        T("Сколько стоит выезд и смета?", "Шығу мен смета қанша тұрады?", "How much does a site visit and estimate cost?"),
        T(
            "Бесплатно по всему Казахстану.",
            "Бүкіл Қазақстан бойынша тегін.",
            "Free across Kazakhstan.",
        ),
    ),
    (
        T("Какая гарантия?", "Қандай кепілдік бар?", "What warranty do you give?"),
        T(
            "Гарантия на монтажные работы — 1 год, на оборудование — по гарантии производителя. Все условия фиксируем в договоре.",
            "Монтаж жұмыстарына кепілдік — 1 жыл, жабдыққа — өндірушінің кепілдігі бойынша. Барлық шарттарды шартта бекітеміз.",
            "1 year on installation work; equipment is covered by the manufacturer's warranty. All terms are in the contract.",
        ),
    ),
    (
        T("Как быстро вы приедете?", "Қаншалықты тез келесіздер?", "How soon can you come?"),
        T(
            "Обычно на замер приезжаем в день обращения или на следующий день. Монтаж квартиры занимает около одного дня.",
            "Әдетте өлшеуге хабарласқан күні немесе келесі күні келеміз. Пәтерге монтаж шамамен бір күн алады.",
            "We usually visit for a survey the same or the next day. An apartment installation takes about one day.",
        ),
    ),
    (
        T("Работаете с юрлицами?", "Заңды тұлғалармен жұмыс істейсіздер ме?", "Do you work with companies?"),
        T(
            "Да, работаем с ТОО и ИП по договору, с безналичной оплатой и закрывающими документами.",
            "Иә, ЖШС және ЖК-мен шарт бойынша, қолма-қол ақшасыз төлеммен және жабу құжаттарымен жұмыс істейміз.",
            "Yes, we work with LLPs and sole proprietors under contract, with bank transfer and closing documents.",
        ),
    ),
]

CASES = [
    {
        "slug": "kvartira-bostandykskiy",
        "services": ["ajax"],
        "amount": 340000,
        "order": 1,
        "title": T("Сигнализация AJAX в трёхкомнатной квартире", "Үш бөлмелі пәтердегі AJAX дабылы", "AJAX alarm in a three-room apartment"),
        "object_type": T("Квартира в ЖК", "ТҮК-дегі пәтер", "Apartment"),
        "district": T("Бостандыкский район", "Бостандық ауданы", "Bostandyk district"),
        "duration": T("1 день", "1 күн", "1 day"),
        "task": T(
            "Владельцы часто уезжают и хотели знать, что дома всё в порядке: без проводов и ремонта, с управлением с телефона.",
            "Иелері жиі сапарға шығады және үйде бәрі жақсы екенін білгісі келді: сымсыз, жөндеусіз, телефоннан басқарумен.",
            "The owners travel often and wanted peace of mind: no wires, no renovation, control from the phone.",
        ),
        "solution": T(
            "Установили 9 устройств AJAX, включая датчик протечки на кухне. Настроили сценарий «Ушёл из дома» и подключили приложение обоим супругам.",
            "9 AJAX құрылғысын, оның ішінде асүйдегі су ағу датчигін орнаттық. «Үйден шықтым» сценарийін баптап, қосымшаны екі жұбайға да қостық.",
            "We installed 9 AJAX devices, including a leak detector in the kitchen, set up a “Leaving home” scenario and connected the app for both spouses.",
        ),
        "equipment": T(
            "Hub 2\n3 датчика движения\n3 датчика открытия\nДатчик протечки\nКлавиатура",
            "Hub 2\n3 қозғалыс датчигі\n3 ашылу датчигі\nСу ағу датчигі\nПернетақта",
            "Hub 2\n3 motion detectors\n3 door/window sensors\nLeak detector\nKeypad",
        ),
    },
    {
        "slug": "dom-nauryzbayskiy",
        "services": ["ajax", "videonablyudenie"],
        "amount": 980000,
        "order": 2,
        "title": T("Частный дом: AJAX и 6 уличных камер", "Жеке үй: AJAX және 6 сыртқы камера", "House: AJAX plus 6 outdoor cameras"),
        "object_type": T("Частный дом 220 м²", "Жеке үй, 220 м²", "House, 220 m²"),
        "district": T("Наурызбайский район", "Наурызбай ауданы", "Nauryzbay district"),
        "duration": T("2 дня", "2 күн", "2 days"),
        "task": T(
            "Нужно было закрыть дом и периметр участка, видеть двор и въезд с телефона.",
            "Үй мен учаске периметрін қорғап, аула мен кіреберісті телефоннан көру қажет болды.",
            "The client needed to protect the house and plot perimeter and see the yard and driveway from the phone.",
        ),
        "solution": T(
            "Поставили AJAX с уличными датчиками движения и 6 камер 4 Мп с ночной съёмкой. При тревоге владелец сразу открывает нужную камеру в телефоне.",
            "Сыртқы қозғалыс датчиктері бар AJAX пен түнгі түсірілімі бар 6 камера (4 Мп) орнаттық. Дабыл кезінде иесі телефонда қажетті камераны бірден ашады.",
            "We installed AJAX with outdoor motion detectors and six 4 MP night-vision cameras. On alarm the owner opens the right camera on the phone right away.",
        ),
        "equipment": T(
            "Hub 2 Plus\n2 уличных датчика движения\n5 датчиков открытия\nУличная сирена\n6 IP-камер 4 Мп\nРегистратор на 8 каналов",
            "Hub 2 Plus\n2 сыртқы қозғалыс датчигі\n5 ашылу датчигі\nСыртқы сирена\n6 IP-камера 4 Мп\n8 арналы тіркеуіш",
            "Hub 2 Plus\n2 outdoor motion detectors\n5 door/window sensors\nOutdoor siren\n6 IP cameras, 4 MP\n8-channel recorder",
        ),
    },
    {
        "slug": "kofeynya-medeuskiy",
        "services": ["videonablyudenie"],
        "amount": 470000,
        "order": 3,
        "title": T("Видеонаблюдение в кофейне", "Кофеханадағы бейнебақылау", "CCTV in a coffee shop"),
        "object_type": T("Кофейня", "Кофехана", "Coffee shop"),
        "district": T("Медеуский район", "Медеу ауданы", "Medeu district"),
        "duration": T("1 день", "1 күн", "1 day"),
        "task": T(
            "Владелец хотел видеть кассу, зал и вход из дома и разбирать спорные ситуации с гостями.",
            "Иесі касса, зал мен кіреберісті үйден көріп, қонақтармен даулы жағдайларды талдағысы келді.",
            "The owner wanted to see the till, the hall and the entrance from home and review disputes with guests.",
        ),
        "solution": T(
            "Установили 8 камер, включая камеру над кассой, тревожную кнопку и удалённый доступ для владельца.",
            "8 камера, оның ішінде касса үстіндегі камера, дабыл түймесін орнатып, иесіне қашықтан кіруді бердік.",
            "We installed 8 cameras, including one over the till, a panic button and remote access for the owner.",
        ),
        "equipment": T(
            "8 IP-камер 4 Мп\nРегистратор\nДиск 2 ТБ\nТревожная кнопка",
            "8 IP-камера 4 Мп\nТіркеуіш\n2 ТБ диск\nДабыл түймесі",
            "8 IP cameras, 4 MP\nRecorder\n2 TB disk\nPanic button",
        ),
    },
    {
        "slug": "ofis-almalinskiy",
        "services": ["skud", "slabotochnye-sistemy"],
        "amount": 1150000,
        "order": 4,
        "title": T("СКУД и локальная сеть в офисе", "Кеңседегі СКУД және жергілікті желі", "Access control and LAN in an office"),
        "object_type": T("Офис 120 м²", "Кеңсе, 120 м²", "Office, 120 m²"),
        "district": T("Алмалинский район", "Алмалы ауданы", "Almaly district"),
        "duration": T("3 дня", "3 күн", "3 days"),
        "task": T(
            "Компания переезжала в новый офис: нужна была сеть на 24 рабочих места и доступ по картам с учётом времени.",
            "Компания жаңа кеңсеге көшті: 24 жұмыс орнына желі және уақытты есепке алатын карта арқылы кіру қажет болды.",
            "The company was moving to a new office and needed a network for 24 workstations and card access with time tracking.",
        ),
        "solution": T(
            "Проложили 24 линии ЛВС, собрали шкаф, настроили Wi-Fi и установили СКУД на 4 двери с учётом рабочего времени.",
            "24 ЖЕЖ желісін тартып, шкафты жинап, Wi-Fi баптадық және жұмыс уақытын есепке алатын 4 есікке СКУД орнаттық.",
            "We ran 24 LAN lines, built the rack, set up Wi-Fi and installed access control on 4 doors with time tracking.",
        ),
        "equipment": T(
            "24 точки ЛВС\nКоммутационный шкаф\n2 точки доступа Wi-Fi\nСКУД на 4 двери",
            "24 ЖЕЖ нүктесі\nКоммутациялық шкаф\n2 Wi-Fi нүктесі\n4 есікке СКУД",
            "24 LAN points\nNetwork rack\n2 Wi-Fi access points\nAccess control for 4 doors",
        ),
    },
    {
        "slug": "sklad-alatauskiy",
        "services": ["videonablyudenie"],
        "amount": 1900000,
        "order": 5,
        "title": T("Склад: 16 камер и охрана периметра", "Қойма: 16 камера және периметр күзеті", "Warehouse: 16 cameras and perimeter alarm"),
        "object_type": T("Склад 1 500 м²", "Қойма, 1 500 м²", "Warehouse, 1,500 m²"),
        "district": T("Алатауский район", "Алатау ауданы", "Alatau district"),
        "duration": T("4 дня", "4 күн", "4 days"),
        "task": T(
            "Нужно было круглосуточно контролировать территорию и погрузку и получать тревоги ночью.",
            "Аумақ пен тиеуді тәулік бойы бақылап, түнде дабыл алу қажет болды.",
            "The client needed 24/7 monitoring of the yard and loading, plus night-time alarms.",
        ),
        "solution": T(
            "Поставили 16 уличных камер с ИК-подсветкой и проводную сигнализацию с выводом на пульт охранной компании.",
            "ИҚ жарығы бар 16 сыртқы камера мен күзет компаниясының пультіне шығатын сымды дабыл орнаттық.",
            "We installed 16 outdoor IR cameras and a wired alarm connected to a security company's monitoring.",
        ),
        "equipment": T(
            "16 уличных IP-камер\nРегистратор на 16 каналов\nДиск 4 ТБ\nПроводная сигнализация\nВывод на пульт",
            "16 сыртқы IP-камера\n16 арналы тіркеуіш\n4 ТБ диск\nСымды дабыл\nПультке шығару",
            "16 outdoor IP cameras\n16-channel recorder\n4 TB disk\nWired alarm\nMonitoring connection",
        ),
    },
    {
        "slug": "butik-v-trc",
        "services": ["ajax", "videonablyudenie"],
        "amount": 520000,
        "order": 6,
        "title": T("Бутик в ТРЦ: AJAX и камеры", "СОО-дағы бутик: AJAX және камералар", "Boutique in a mall: AJAX and cameras"),
        "object_type": T("Бутик", "Бутик", "Boutique"),
        "district": T("Бостандыкский район", "Бостандық ауданы", "Bostandyk district"),
        "duration": T("1 день", "1 күн", "1 day"),
        "task": T(
            "Ночью магазин закрыт: важно сразу узнать о проникновении и увидеть, что происходит.",
            "Түнде дүкен жабық: кіру туралы бірден біліп, не болып жатқанын көру маңызды.",
            "The shop is closed at night; the owner needed instant break-in alerts and video.",
        ),
        "solution": T(
            "Установили AJAX с датчиками на витрину и дверь и 4 камеры. При тревоге владелец сразу открывает видео в телефоне.",
            "Витрина мен есікке датчиктері бар AJAX және 4 камера орнаттық. Дабыл кезінде иесі телефонда бейнені бірден ашады.",
            "We installed AJAX with sensors on the window and door plus 4 cameras. On alarm the owner opens the video on the phone right away.",
        ),
        "equipment": T(
            "Hub 2\nДатчик разбития стекла\n2 датчика открытия\n2 датчика движения\n4 IP-камеры",
            "Hub 2\nӘйнек сыну датчигі\n2 ашылу датчигі\n2 қозғалыс датчигі\n4 IP-камера",
            "Hub 2\nGlass-break detector\n2 door/window sensors\n2 motion detectors\n4 IP cameras",
        ),
    },
]


def pages(brand: str) -> list[dict]:
    return [
        {
            "slug": "o-kompanii",
            "title": T("О компании", "Компания туралы", "About us"),
            "lead": T(
                f"{brand} — команда инженеров-монтажников по всему Казахстану. Устанавливаем охранные системы, видеонаблюдение, СКУД и слаботочные сети.",
                f"{brand} — Қазақстандағы инженер-монтаждаушылар командасы. Күзет жүйелерін, бейнебақылауды, СКУД пен әлсіз ток желілерін орнатамыз.",
                f"{brand} is a team of installation engineers in Kazakhstan. We install security systems, CCTV, access control and low-voltage networks.",
            ),
            "body": T(
                "<h2>Чем мы занимаемся</h2><p>Проектируем и монтируем системы безопасности для квартир, домов, офисов, магазинов и складов. "
                "Работаем с беспроводными и проводными системами, IP-видеонаблюдением, контролем доступа и кабельными сетями.</p>"
                "<h2>Как мы работаем</h2><ul><li>Бесплатный выезд и смета до начала работ</li><li>Договор с фиксированной ценой</li>"
                "<li>Аккуратный монтаж и уборка после себя</li><li>Обучение и поддержка после установки</li></ul>"
                "<h2>Где работаем</h2><p>По всему Казахстану: в любом городе есть монтажные бригады, инженеры, техники и КУЗЕТ.</p>",
                "<h2>Немен айналысамыз</h2><p>Пәтерлерге, үйлерге, кеңселерге, дүкендер мен қоймаларға қауіпсіздік жүйелерін жобалап, орнатамыз. "
                "Сымсыз және сымды жүйелермен, IP-бейнебақылаумен, кіруді бақылаумен және кабель желілерімен жұмыс істейміз.</p>"
                "<h2>Қалай жұмыс істейміз</h2><ul><li>Жұмыс басталғанға дейін тегін шығу және смета</li><li>Бекітілген бағамен шарт</li>"
                "<li>Мұқият монтаж және соңынан жинастыру</li><li>Орнатқаннан кейін оқыту және қолдау</li></ul>"
                "<h2>Қай жерде жұмыс істейміз</h2><p>Бүкіл Қазақстан бойынша: кез келген қалада монтаж бригадалары, инженерлер, техниктер және КҮЗЕТ бар.</p>",
                "<h2>What we do</h2><p>We design and install security systems for apartments, houses, offices, shops and warehouses. "
                "We work with wireless and wired systems, IP video surveillance, access control and structured cabling.</p>"
                "<h2>How we work</h2><ul><li>Free site visit and estimate before any work</li><li>Fixed-price contract</li>"
                "<li>Neat installation and clean-up afterwards</li><li>Training and support after installation</li></ul>"
                "<h2>Where we work</h2><p>All over Kazakhstan: installation crews, engineers, technicians and KUZET (Security) are available in every city.</p>",
            ),
        },
        {
            "slug": "privacy",
            "title": T("Политика конфиденциальности", "Құпиялылық саясаты", "Privacy policy"),
            "lead": T(
                "Как мы собираем, используем и храним персональные данные посетителей сайта.",
                "Сайтқа келушілердің дербес деректерін қалай жинайтынымыз, пайдаланатынымыз және сақтайтынымыз.",
                "How we collect, use and store the personal data of website visitors.",
            ),
            "body": T(
                f"<p>Политика составлена в соответствии с Законом Республики Казахстан «О персональных данных и их защите». Оператор данных — {brand}.</p>"
                "<h2>Какие данные мы собираем</h2><ul><li>Имя и номер телефона, которые вы указываете в форме заявки</li>"
                "<li>Сведения об объекте и комментарий к заявке</li><li>Технические данные: IP-адрес, тип браузера, страница заявки, рекламные метки (UTM, gclid, yclid), cookie сервисов аналитики</li></ul>"
                "<h2>Зачем</h2><ul><li>Связаться с вами, рассчитать стоимость и выполнить работы</li><li>Заключить и исполнить договор</li><li>Улучшать сайт и оценивать эффективность рекламы</li></ul>"
                "<h2>Хранение и защита</h2><p>Данные хранятся на серверах, расположенных в Республике Казахстан, доступ к ним есть только у сотрудников, которые обрабатывают заявки. "
                "Мы храним данные, пока это нужно для целей обработки или требуется по закону.</p>"
                "<h2>Передача третьим лицам</h2><p>Мы не продаём и не передаём ваши данные третьим лицам, кроме случаев, предусмотренных законом. "
                "На сайте работают сервисы аналитики (Google Analytics, Яндекс Метрика), которые получают обезличенные технические данные.</p>"
                "<h2>Ваши права</h2><p>Вы можете запросить сведения о ваших данных, их исправление или удаление и отозвать согласие, написав нам по контактам, указанным на сайте.</p>",
                f"<p>Саясат Қазақстан Республикасының «Дербес деректер және оларды қорғау туралы» Заңына сәйкес жасалған. Деректер операторы — {brand}.</p>"
                "<h2>Қандай деректерді жинаймыз</h2><ul><li>Өтінім нысанында көрсететін атыңыз бен телефон нөміріңіз</li>"
                "<li>Нысан туралы мәліметтер және өтінімге түсініктеме</li><li>Техникалық деректер: IP-мекенжай, браузер түрі, өтінім беті, жарнамалық белгілер (UTM, gclid, yclid), аналитика қызметтерінің cookie файлдары</li></ul>"
                "<h2>Не үшін</h2><ul><li>Сізбен байланысу, құнын есептеу және жұмысты орындау</li><li>Шарт жасасу және оны орындау</li><li>Сайтты жақсарту және жарнаманың тиімділігін бағалау</li></ul>"
                "<h2>Сақтау және қорғау</h2><p>Деректер Қазақстан Республикасында орналасқан серверлерде сақталады, оларға тек өтінімдерді өңдейтін қызметкерлердің қолжетімділігі бар. "
                "Деректерді өңдеу мақсаттары үшін қажет болғанша немесе заң талап еткенше сақтаймыз.</p>"
                "<h2>Үшінші тұлғаларға беру</h2><p>Заңда көзделген жағдайлардан басқа, деректеріңізді үшінші тұлғаларға сатпаймыз және бермейміз. "
                "Сайтта иесіздендірілген техникалық деректерді алатын аналитика қызметтері (Google Analytics, Яндекс Метрика) жұмыс істейді.</p>"
                "<h2>Сіздің құқықтарыңыз</h2><p>Сайтта көрсетілген байланыстар арқылы жазып, деректеріңіз туралы мәлімет сұрай аласыз, оларды түзетуді немесе жоюды талап етіп, келісіміңізді кері қайтара аласыз.</p>",
                f"<p>This policy follows the Law of the Republic of Kazakhstan “On Personal Data and Their Protection”. The data controller is {brand}.</p>"
                "<h2>What we collect</h2><ul><li>The name and phone number you enter in the request form</li>"
                "<li>Details about your property and comments on the request</li><li>Technical data: IP address, browser type, request page, ad tags (UTM, gclid, yclid), analytics cookies</li></ul>"
                "<h2>Why</h2><ul><li>To contact you, prepare an estimate and carry out the work</li><li>To conclude and perform a contract</li><li>To improve the website and measure advertising effectiveness</li></ul>"
                "<h2>Storage and protection</h2><p>Data is stored on servers located in the Republic of Kazakhstan and is accessible only to staff who handle requests. "
                "We keep data as long as needed for these purposes or as required by law.</p>"
                "<h2>Sharing with third parties</h2><p>We do not sell or share your data with third parties except as required by law. "
                "The website uses analytics services (Google Analytics, Yandex Metrica) that receive anonymised technical data.</p>"
                "<h2>Your rights</h2><p>You can request information about your data, its correction or deletion, and withdraw your consent by contacting us using the details on this website.</p>",
            ),
        },
    ]
