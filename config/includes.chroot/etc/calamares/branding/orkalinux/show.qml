import QtQuick 2.0;
import calamares.slideshow 1.0;
import io.calamares.ui 1.0

Presentation
{
    id: presentation

    readonly property string lang: {
        var b = ViewManager.backLabel.replace("&", "");
        var known = { "Wstecz": "pl", "Zurück": "de", "Précédent": "fr", "Atrás": "es",
                      "Indietro": "it", "Voltar": "pt", "Назад": "uk" };
        return known[b] || "en";
    }

    readonly property var texts: ({
        "en": [
            ["Welcome to OrkaLinux", "Sit back, the installer does the rest. It usually takes a few minutes, depending on your disk. When it's done, restart, log in and OrkaLinux Hello will show you around."],
            ["Dark or light", "OrkaLinux comes in a dark and a light version. Switch between them in OrkaLinux Appearance or at the bottom of Hello. The Undertow wallpaper, the apps and the installer all follow along."],
            ["Thousands of apps", "Discover comes with Flathub, so there's a huge library of apps one click away. Steam, OBS, GIMP, Spotify and more are also in Hello under More software, ready to tick and install."],
            ["kitty terminal", "A fast terminal with a see-through, blurred background, a cursor trail and a colourful prompt. Type fastfetch to show off your system. Commands you need sudo for will ask for your password."],
            ["Ready to play", "If you have an NVIDIA card, OrkaLinux Center installs the right driver for you. Then grab Steam or Heroic from More software. Proton runs most Windows games without any setup."],
            ["Come say hi", "OrkaLinux is made by one person, _inc0gnit0. Found a bug, have an idea or just want to chat? Drop by the OrkaLinux Discord, every message helps make the next version better."],
            ["Your desktop, your way", "OrkaLinux Appearance changes the panel in one click: the OrkaLinux bar, a Windows-like or macOS-like layout, or the classic one. Colours, accent and wallpapers are right next to it."],
            ["Something broke? Go back in time", "OrkaLinux Backup takes restore points of the system, every day and before updates. If something stops working, pick a point and restore. Your own files in the home folder are never touched."],
            ["Everything in one place", "OrkaLinux Center shows what's in your computer and gathers the important settings: network, sound, displays, drivers, the kernel and cleanup. No more hunting through menus."],
            ["Debian underneath", "Under the hood is Debian 13, one of the most stable systems out there, with a newer kernel for recent hardware. No ads, no tracking, no accounts you have to make."],
            ["Pick your login screen", "Don't like the standard one? In OrkaLinux Appearance, under Login, choose between Plasma, Glass with a big clock, or a dark side panel. A preview shows each one before you switch."],
            ["Boot screen too", "While the computer starts you see the OrkaLinux logo with a thin loading bar. Prefer spinning dots near the bottom? Switch it in OrkaLinux Appearance, under Boot."],
            ["AI apps one click away", "More software in Hello now has an AI group: the Claude app, Claude Code and Codex. Tick them and they install from their makers' official sources, so they stay up to date."],
            ["Updates without the hassle", "OrkaLinux Center tells you when updates are waiting and installs system packages and Flatpak apps in one go. Before updating, Backup can make a restore point, just in case."]
        ],
        "pl": [
            ["Witaj w OrkaLinux", "Rozsiądź się, instalator zrobi resztę. Zwykle trwa to kilka minut, zależnie od dysku. Potem uruchom ponownie, zaloguj się, a OrkaLinux Hello pokaże Ci, co i gdzie."],
            ["Ciemny albo jasny", "OrkaLinux ma wersję ciemną i jasną. Przełączasz je w Wyglądzie systemu OrkaLinux albo na dole okna Hello. Tapeta Undertow, programy i instalator zmieniają się razem z nimi."],
            ["Tysiące programów", "Discover ma Flathuba, więc ogromna biblioteka programów jest na jedno kliknięcie. Steam, OBS, GIMP, Spotify i reszta czekają też w Hello, w Dodatkowych programach: zaznaczasz i gotowe."],
            ["Terminal kitty", "Szybki terminal z przezroczystym, rozmytym tłem, smugą za kursorem i kolorowym promptem. Wpisz fastfetch, żeby pochwalić się systemem. Polecenia z sudo zapytają o Twoje hasło."],
            ["Gotowy do grania", "Masz kartę NVIDIA? Centrum OrkaLinux samo zainstaluje właściwy sterownik. Potem Steam albo Heroic z Dodatkowych programów, a Proton odpali większość gier z Windowsa bez kombinowania."],
            ["Wpadnij na Discorda", "OrkaLinux robi jedna osoba, _inc0gnit0. Znalazłeś błąd, masz pomysł albo chcesz po prostu pogadać? Wbijaj na Discorda OrkaLinux, każda wiadomość pomaga zrobić lepszą następną wersję."],
            ["Pulpit po Twojemu", "Wygląd systemu OrkaLinux zmienia panel jednym kliknięciem: pasek OrkaLinux, układ jak w Windowsie, jak w macOS albo klasyczny. Kolory, akcent i tapety są zaraz obok."],
            ["Coś się zepsuło? Cofnij czas", "Kopia zapasowa OrkaLinux robi punkty przywracania systemu, codziennie i przed aktualizacjami. Jak coś przestanie działać, wybierasz punkt i przywracasz. Twoich plików w katalogu domowym nie rusza."],
            ["Wszystko w jednym miejscu", "Centrum OrkaLinux pokazuje, co masz w komputerze, i zbiera najważniejsze ustawienia: sieć, dźwięk, ekrany, sterowniki, jądro i sprzątanie. Koniec z szukaniem po menu."],
            ["Pod spodem Debian", "Pod maską jest Debian 13, jeden z najstabilniejszych systemów, do tego nowsze jądro dla nowego sprzętu. Bez reklam, bez śledzenia i bez zakładania kont."],
            ["Wybierz ekran logowania", "Standardowy Ci nie leży? W Wyglądzie systemu OrkaLinux, w zakładce Logowanie, wybierasz: Plasma, Szkło z dużym zegarem albo ciemny panel z boku. Każdy ma podgląd, zanim go włączysz."],
            ["Ekran startowy też", "Gdy komputer się uruchamia, widać logo OrkaLinux i cienki pasek ładowania. Wolisz kręcące się kropki na dole? Zmienisz to w Wyglądzie systemu OrkaLinux, w zakładce Uruchamianie."],
            ["Programy AI na kliknięcie", "W Dodatkowych programach w Hello jest grupa AI: aplikacja Claude, Claude Code i Codex. Zaznaczasz, a instalują się z oficjalnych źródeł twórców, więc same się aktualizują."],
            ["Aktualizacje bez kombinowania", "Centrum OrkaLinux mówi, kiedy czekają aktualizacje, i instaluje paczki systemu oraz programy z Flatpaka za jednym razem. Przed aktualizacją Kopia zapasowa może zrobić punkt przywracania, tak na wszelki wypadek."]
        ],
        "de": [
            ["Willkommen bei OrkaLinux", "Lehn dich zurück, der Installer macht den Rest. Das dauert meist ein paar Minuten, je nach Festplatte. Danach neu starten, anmelden, und OrkaLinux Hello zeigt dir alles."],
            ["Dunkel oder hell", "OrkaLinux gibt es dunkel und hell. Du wechselst in OrkaLinux Aussehen oder unten in Hello. Das Undertow-Hintergrundbild, die Programme und der Installer passen sich an."],
            ["Tausende Programme", "Discover hat Flathub, also eine riesige Auswahl an Programmen mit einem Klick. Steam, OBS, GIMP, Spotify und mehr findest du auch in Hello unter Weitere Programme."],
            ["kitty-Terminal", "Ein schnelles Terminal mit durchsichtigem, unscharfem Hintergrund, Cursor-Spur und buntem Prompt. Tipp fastfetch, um dein System zu zeigen. Befehle mit sudo fragen nach deinem Passwort."],
            ["Bereit zum Zocken", "Mit einer NVIDIA-Karte installiert das OrkaLinux Zentrum den passenden Treiber. Dann Steam oder Heroic aus Weitere Programme holen. Proton startet die meisten Windows-Spiele ohne Einrichtung."],
            ["Sag hallo", "OrkaLinux wird von einer Person gemacht: _inc0gnit0. Einen Fehler gefunden, eine Idee oder einfach Lust zu quatschen? Komm auf den OrkaLinux-Discord, jede Nachricht macht die nächste Version besser."],
            ["Dein Desktop, wie du willst", "OrkaLinux Aussehen wechselt die Leiste mit einem Klick: die OrkaLinux-Leiste, wie Windows, wie macOS oder klassisch. Farben, Akzent und Hintergründe gleich daneben."],
            ["Etwas kaputt? Zurück in der Zeit", "OrkaLinux Sicherung erstellt Wiederherstellungspunkte, täglich und vor Updates. Wenn etwas nicht mehr geht, wählst du einen Punkt und stellst ihn wieder her. Deine eigenen Dateien bleiben unberührt."],
            ["Alles an einem Ort", "Das OrkaLinux Zentrum zeigt, was in deinem Computer steckt, und sammelt die wichtigen Einstellungen: Netzwerk, Ton, Bildschirme, Treiber, Kernel und Aufräumen. Kein Suchen mehr in Menüs."],
            ["Darunter Debian", "Unter der Haube steckt Debian 13, eines der stabilsten Systeme überhaupt, mit neuerem Kernel für aktuelle Hardware. Keine Werbung, kein Tracking, keine Pflichtkonten."],
            ["Wähle deinen Anmeldebildschirm", "Der Standard gefällt dir nicht? In OrkaLinux Aussehen unter Anmeldung wählst du Plasma, Glas mit großer Uhr oder eine dunkle Seitenleiste. Eine Vorschau zeigt jeden vorher."],
            ["Auch der Startbildschirm", "Beim Hochfahren siehst du das OrkaLinux-Logo mit einem dünnen Ladebalken. Lieber kreisende Punkte unten? Das stellst du in OrkaLinux Aussehen unter Start um."],
            ["KI-Programme mit einem Klick", "In Hello gibt es unter Weitere Programme jetzt eine KI-Gruppe: die Claude-App, Claude Code und Codex. Sie kommen aus den offiziellen Quellen der Hersteller und bleiben aktuell."],
            ["Updates ohne Stress", "Das OrkaLinux Zentrum zeigt, wenn Updates warten, und installiert Systempakete und Flatpak-Apps auf einmal. Vorher kann die Sicherung einen Wiederherstellungspunkt anlegen, nur für den Fall."]
        ],
        "fr": [
            ["Bienvenue dans OrkaLinux", "Installe-toi confortablement, l'installateur fait le reste. Ça prend en général quelques minutes selon ton disque. Ensuite, redémarre, connecte-toi et OrkaLinux Hello te fera faire le tour."],
            ["Sombre ou clair", "OrkaLinux existe en version sombre et claire. Change-la dans Apparence OrkaLinux ou en bas de Hello. Le fond d'écran Undertow, les applis et l'installateur suivent."],
            ["Des milliers d'applis", "Discover inclut Flathub, donc une énorme bibliothèque d'applis à portée de clic. Steam, OBS, GIMP, Spotify et d'autres sont aussi dans Hello, dans Plus de logiciels."],
            ["Terminal kitty", "Un terminal rapide au fond transparent et flouté, avec une traînée du curseur et un prompt coloré. Tape fastfetch pour frimer avec ton système. Les commandes avec sudo demandent ton mot de passe."],
            ["Prêt à jouer", "Avec une carte NVIDIA, le Centre OrkaLinux installe le bon pilote pour toi. Ajoute ensuite Steam ou Heroic depuis Plus de logiciels. Proton lance la plupart des jeux Windows sans réglage."],
            ["Viens dire salut", "OrkaLinux est fait par une seule personne, _inc0gnit0. Un bug, une idée ou juste envie de discuter ? Passe sur le Discord OrkaLinux, chaque message aide à améliorer la prochaine version."],
            ["Ton bureau, à ta façon", "Apparence OrkaLinux change la barre en un clic : la barre OrkaLinux, façon Windows, façon macOS ou classique. Couleurs, accent et fonds d'écran juste à côté."],
            ["Un souci ? Remonte le temps", "Sauvegarde OrkaLinux crée des points de restauration, chaque jour et avant les mises à jour. Si quelque chose ne marche plus, choisis un point et restaure. Tes fichiers personnels ne sont jamais touchés."],
            ["Tout au même endroit", "Le Centre OrkaLinux montre ce qu'il y a dans ton ordinateur et regroupe les réglages importants : réseau, son, écrans, pilotes, noyau et nettoyage. Fini de chercher dans les menus."],
            ["Debian en dessous", "Sous le capot, Debian 13, l'un des systèmes les plus stables, avec un noyau plus récent pour le matériel récent. Pas de pub, pas de pistage, pas de compte obligatoire."],
            ["Choisis ton écran de connexion", "L'écran standard ne te plaît pas ? Dans Apparence OrkaLinux, onglet Connexion, choisis Plasma, Verre avec une grande horloge ou un panneau latéral sombre. Un aperçu montre chacun avant."],
            ["L'écran de démarrage aussi", "Au démarrage, tu vois le logo OrkaLinux avec une fine barre de chargement. Tu préfères des points qui tournent en bas ? Change-le dans Apparence OrkaLinux, onglet Démarrage."],
            ["Des applis IA en un clic", "Plus de logiciels, dans Hello, a maintenant un groupe IA : l'appli Claude, Claude Code et Codex. Elles viennent des sources officielles de leurs créateurs et restent à jour."],
            ["Des mises à jour sans prise de tête", "Le Centre OrkaLinux te dit quand des mises à jour attendent et installe paquets système et applis Flatpak d'un coup. Avant, Sauvegarde peut créer un point de restauration, au cas où."]
        ],
        "es": [
            ["Bienvenido a OrkaLinux", "Ponte cómodo, el instalador hace el resto. Suele tardar unos minutos, según el disco. Cuando termine, reinicia, inicia sesión y OrkaLinux Hello te enseñará dónde está todo."],
            ["Oscuro o claro", "OrkaLinux viene en versión oscura y clara. Cámbiala en Apariencia de OrkaLinux o abajo en Hello. El fondo Undertow, las aplicaciones y el instalador se cambian con ella."],
            ["Miles de aplicaciones", "Discover trae Flathub, así que tienes una enorme biblioteca de aplicaciones a un clic. Steam, OBS, GIMP, Spotify y más también están en Hello, en Más programas: marcas y listo."],
            ["Terminal kitty", "Un terminal rápido con fondo transparente y difuminado, estela del cursor y un prompt de colores. Escribe fastfetch para presumir de sistema. Los comandos con sudo te pedirán la contraseña."],
            ["Listo para jugar", "¿Tienes una tarjeta NVIDIA? El Centro OrkaLinux instala el controlador correcto por ti. Luego coge Steam o Heroic en Más programas. Proton abre la mayoría de juegos de Windows sin configurar nada."],
            ["Pasa a saludar", "OrkaLinux lo hace una sola persona, _inc0gnit0. ¿Has encontrado un fallo, tienes una idea o solo quieres charlar? Pásate por el Discord de OrkaLinux, cada mensaje ayuda a mejorar la próxima versión."],
            ["Tu escritorio, a tu manera", "Apariencia de OrkaLinux cambia el panel con un clic: la barra de OrkaLinux, estilo Windows, estilo macOS o la clásica. Colores, acento y fondos de pantalla justo al lado."],
            ["¿Algo se ha roto? Vuelve atrás en el tiempo", "Copia de seguridad OrkaLinux crea puntos de restauración del sistema, cada día y antes de las actualizaciones. Si algo deja de funcionar, eliges un punto y restauras. Tus archivos personales no se tocan."],
            ["Todo en un solo sitio", "El Centro OrkaLinux muestra lo que hay en tu ordenador y reúne los ajustes importantes: red, sonido, pantallas, controladores, el kernel y la limpieza. Se acabó buscar por los menús."],
            ["Debian por debajo", "Por dentro está Debian 13, uno de los sistemas más estables que hay, con un kernel más nuevo para el hardware reciente. Sin anuncios, sin rastreo y sin cuentas obligatorias."],
            ["Elige tu pantalla de inicio de sesión", "¿No te gusta la de siempre? En Apariencia de OrkaLinux eliges entre Plasma, Cristal con un reloj grande o un panel lateral oscuro. Cada una tiene vista previa antes de cambiar."],
            ["La pantalla de arranque también", "Mientras arranca el ordenador ves el logo de OrkaLinux con una barra de carga fina. ¿Prefieres puntos girando abajo? Cámbialo en Apariencia de OrkaLinux."],
            ["Aplicaciones de IA a un clic", "Más programas, en Hello, ahora tiene un grupo de IA: la aplicación Claude, Claude Code y Codex. Se instalan desde las fuentes oficiales de sus creadores, así que se mantienen al día."],
            ["Actualizaciones sin complicaciones", "El Centro OrkaLinux te avisa cuando hay actualizaciones e instala los paquetes del sistema y las aplicaciones Flatpak de una vez. Antes, Copia de seguridad puede crear un punto de restauración, por si acaso."]
        ],
        "it": [
            ["Benvenuto in OrkaLinux", "Mettiti comodo, l'installer fa il resto. Di solito ci vogliono pochi minuti, a seconda del disco. Alla fine riavvia, accedi e OrkaLinux Hello ti mostrerà dove si trova tutto."],
            ["Scuro o chiaro", "OrkaLinux ha una versione scura e una chiara. Cambiala in Aspetto di OrkaLinux o in fondo a Hello. Lo sfondo Undertow, le app e l'installer cambiano insieme."],
            ["Migliaia di app", "Discover ha Flathub, quindi un'enorme libreria di app è a un clic. Steam, OBS, GIMP, Spotify e altro sono anche in Hello, in Altri programmi: spunti e fatto."],
            ["Terminale kitty", "Un terminale veloce con sfondo trasparente e sfocato, scia del cursore e prompt colorato. Scrivi fastfetch per mettere in mostra il sistema. I comandi con sudo ti chiedono la password."],
            ["Pronto per giocare", "Hai una scheda NVIDIA? Il Centro OrkaLinux installa il driver giusto per te. Poi prendi Steam o Heroic da Altri programmi. Proton avvia la maggior parte dei giochi Windows senza configurare nulla."],
            ["Passa a salutare", "OrkaLinux è fatto da una sola persona, _inc0gnit0. Hai trovato un bug, hai un'idea o vuoi solo fare due chiacchiere? Passa sul Discord di OrkaLinux, ogni messaggio aiuta a migliorare la prossima versione."],
            ["Il tuo desktop, a modo tuo", "Aspetto di OrkaLinux cambia il pannello con un clic: la barra di OrkaLinux, stile Windows, stile macOS o quella classica. Colori, accento e sfondi sono lì accanto."],
            ["Si è rotto qualcosa? Torna indietro nel tempo", "Backup di OrkaLinux crea punti di ripristino del sistema, ogni giorno e prima degli aggiornamenti. Se qualcosa smette di funzionare, scegli un punto e ripristini. I tuoi file personali non vengono toccati."],
            ["Tutto in un posto", "Il Centro OrkaLinux mostra cosa c'è nel tuo computer e raccoglie le impostazioni importanti: rete, audio, schermi, driver, kernel e pulizia. Basta cercare nei menu."],
            ["Sotto c'è Debian", "Sotto il cofano c'è Debian 13, uno dei sistemi più stabili in circolazione, con un kernel più nuovo per l'hardware recente. Niente pubblicità, niente tracciamento, niente account obbligatori."],
            ["Scegli la schermata di accesso", "Quella standard non ti piace? In Aspetto di OrkaLinux scegli tra Plasma, Vetro con un grande orologio o un pannello laterale scuro. Ognuna ha un'anteprima prima di passare."],
            ["Anche la schermata di avvio", "Mentre il computer si avvia vedi il logo di OrkaLinux con una sottile barra di caricamento. Preferisci dei puntini che girano in basso? Lo cambi in Aspetto di OrkaLinux."],
            ["App di IA a un clic", "Altri programmi, in Hello, ora ha un gruppo IA: l'app Claude, Claude Code e Codex. Si installano dalle fonti ufficiali dei loro autori, quindi restano aggiornate."],
            ["Aggiornamenti senza pensieri", "Il Centro OrkaLinux ti avvisa quando ci sono aggiornamenti e installa i pacchetti di sistema e le app Flatpak in un colpo solo. Prima, Backup può creare un punto di ripristino, non si sa mai."]
        ],
        "pt": [
            ["Boas-vindas ao OrkaLinux", "Relaxe, o instalador faz o resto. Normalmente leva alguns minutos, dependendo do disco. Quando terminar, reinicie, entre e o OrkaLinux Hello vai mostrar onde fica cada coisa."],
            ["Escuro ou claro", "O OrkaLinux vem em versão escura e clara. Troque em Aparência do OrkaLinux ou no rodapé do Hello. O papel de parede Undertow, os aplicativos e o instalador acompanham."],
            ["Milhares de aplicativos", "O Discover vem com o Flathub, então uma biblioteca enorme de aplicativos fica a um clique. Steam, OBS, GIMP, Spotify e outros também estão no Hello, em Mais programas: é só marcar."],
            ["Terminal kitty", "Um terminal rápido com fundo transparente e desfocado, rastro do cursor e prompt colorido. Digite fastfetch para exibir seu sistema. Comandos com sudo vão pedir sua senha."],
            ["Pronto para jogar", "Tem placa NVIDIA? A Central OrkaLinux instala o driver certo para você. Depois pegue o Steam ou o Heroic em Mais programas. O Proton roda a maioria dos jogos de Windows sem configurar nada."],
            ["Venha dar um oi", "O OrkaLinux é feito por uma pessoa só, _inc0gnit0. Achou um bug, tem uma ideia ou só quer conversar? Passe no Discord do OrkaLinux, cada mensagem ajuda a melhorar a próxima versão."],
            ["Sua área de trabalho, do seu jeito", "Aparência do OrkaLinux troca o painel com um clique: a barra do OrkaLinux, estilo Windows, estilo macOS ou a clássica. Cores, destaque e papéis de parede estão logo ao lado."],
            ["Algo quebrou? Volte no tempo", "O Backup do OrkaLinux cria pontos de restauração do sistema, todo dia e antes das atualizações. Se algo parar de funcionar, escolha um ponto e restaure. Seus arquivos pessoais não são tocados."],
            ["Tudo em um só lugar", "A Central OrkaLinux mostra o que tem no seu computador e reúne as configurações importantes: rede, som, telas, drivers, kernel e limpeza. Chega de procurar nos menus."],
            ["Debian por baixo", "Por baixo está o Debian 13, um dos sistemas mais estáveis que existem, com um kernel mais novo para hardware recente. Sem anúncios, sem rastreamento e sem contas obrigatórias."],
            ["Escolha sua tela de login", "Não curtiu a padrão? Em Aparência do OrkaLinux você escolhe entre Plasma, Vidro com um relógio grande ou um painel lateral escuro. Cada uma tem prévia antes de trocar."],
            ["A tela de inicialização também", "Enquanto o computador liga você vê o logo do OrkaLinux com uma barra de carregamento fina. Prefere pontinhos girando embaixo? Troque em Aparência do OrkaLinux."],
            ["Apps de IA a um clique", "Mais programas, no Hello, agora tem um grupo de IA: o app Claude, o Claude Code e o Codex. Eles vêm das fontes oficiais dos criadores, então ficam sempre atualizados."],
            ["Atualizações sem dor de cabeça", "A Central OrkaLinux avisa quando há atualizações e instala os pacotes do sistema e os apps Flatpak de uma vez. Antes, o Backup pode criar um ponto de restauração, só por garantia."]
        ],
        "uk": [
            ["Вітаємо в OrkaLinux", "Влаштовуйтеся зручніше, встановлювач зробить решту. Зазвичай це займає кілька хвилин, залежно від диска. Потім перезапустіть, увійдіть, і OrkaLinux Hello покаже, що де."],
            ["Темний або світлий", "OrkaLinux має темну й світлу версії. Перемикайте їх у Вигляді OrkaLinux або внизу вікна Hello. Шпалери Undertow, програми й встановлювач змінюються разом з ними."],
            ["Тисячі програм", "Discover має Flathub, тож величезна бібліотека програм за один клік. Steam, OBS, GIMP, Spotify та інше також є в Hello, у розділі Більше програм: позначте і готово."],
            ["Термінал kitty", "Швидкий термінал із прозорим розмитим тлом, слідом курсора й кольоровим рядком. Введіть fastfetch, щоб похизуватися системою. Команди з sudo запитають ваш пароль."],
            ["Готові грати", "Маєте відеокарту NVIDIA? Центр OrkaLinux сам встановить потрібний драйвер. Потім візьміть Steam або Heroic у Більше програм. Proton запускає більшість ігор для Windows без налаштувань."],
            ["Заходьте привітатися", "OrkaLinux робить одна людина, _inc0gnit0. Знайшли помилку, маєте ідею чи просто хочете поговорити? Заходьте в Discord OrkaLinux, кожне повідомлення допомагає зробити наступну версію кращою."],
            ["Ваша стільниця, як вам зручно", "Вигляд OrkaLinux змінює панель одним клацанням: панель OrkaLinux, як у Windows, як у macOS або класична. Кольори, акцент і шпалери поруч."],
            ["Щось зламалося? Поверніться в минуле", "Резервні копії OrkaLinux створюють точки відновлення системи щодня і перед оновленнями. Якщо щось перестане працювати, виберіть точку й відновіть. Ваші власні файли не зачіпаються."],
            ["Усе в одному місці", "Центр OrkaLinux показує, що є у вашому комп'ютері, і збирає важливі налаштування: мережу, звук, екрани, драйвери, ядро й очищення. Більше не треба шукати по меню."],
            ["Під капотом Debian", "Під капотом Debian 13, одна з найстабільніших систем, з новішим ядром для сучасного заліза. Без реклами, без стеження і без обов'язкових акаунтів."],
            ["Оберіть екран входу", "Стандартний не подобається? У Вигляді OrkaLinux оберіть Plasma, Скло з великим годинником або темну бічну панель. Кожен має попередній перегляд."],
            ["І екран запуску теж", "Під час запуску ви бачите логотип OrkaLinux із тонкою смугою завантаження. Більше подобаються крапки, що крутяться внизу? Змініть це у Вигляді OrkaLinux."],
            ["Програми ШІ в один клік", "У Більше програм у Hello тепер є група ШІ: застосунок Claude, Claude Code і Codex. Вони встановлюються з офіційних джерел розробників, тож самі оновлюються."],
            ["Оновлення без клопоту", "Центр OrkaLinux повідомляє, коли чекають оновлення, і встановлює системні пакунки та програми Flatpak за один раз. Перед цим Резервні копії можуть створити точку відновлення, про всяк випадок."]
        ]
    })

    Timer {
        interval: 14000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Rectangle {
        anchors.fill: parent
        color: "#0f1120"
        z: -2
    }
    Image {
        anchors.fill: parent
        z: -1
        source: "slide" + (presentation.currentSlide + 1) + ".jpg"
        fillMode: Image.PreserveAspectCrop
        horizontalAlignment: Image.AlignRight
        verticalAlignment: Image.AlignBottom
        smooth: true
    }

    readonly property real imageWidth: Math.max(width, height * 1200 / 560)
    readonly property real graphicLeft: width - imageWidth * 0.51
    readonly property real textLeft: Math.max(32, width * 0.06)
    readonly property real textWidth: Math.max(260, Math.min(width * 0.42, graphicLeft - textLeft - 36))

    component OrkaSlide: Slide {
        property int n: 0

        Column {
            anchors.left: parent.left
            anchors.leftMargin: presentation.textLeft
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -parent.height * 0.07
            width: presentation.textWidth
            spacing: 14

            Rectangle {
                width: 36
                height: 4
                radius: 2
                color: "#4f58f0"
            }
            Text {
                width: parent.width
                text: presentation.texts[presentation.lang][n][0]
                color: "#ffffff"
                font.pointSize: presentation.textWidth < 340 ? 19 : 22
                font.bold: true
                wrapMode: Text.WordWrap
            }
            Text {
                width: parent.width
                text: presentation.texts[presentation.lang][n][1]
                color: "#a0a6c4"
                font.pointSize: 11.5
                lineHeight: 1.3
                wrapMode: Text.WordWrap
            }
        }
    }

    OrkaSlide { n: 0 }
    OrkaSlide { n: 1 }
    OrkaSlide { n: 2 }
    OrkaSlide { n: 3 }
    OrkaSlide { n: 4 }
    OrkaSlide { n: 5 }
    OrkaSlide { n: 6 }
    OrkaSlide { n: 7 }
    OrkaSlide { n: 8 }
    OrkaSlide { n: 9 }
    OrkaSlide { n: 10 }
    OrkaSlide { n: 11 }
    OrkaSlide { n: 12 }
    OrkaSlide { n: 13 }

    function onActivate() { presentation.currentSlide = 0; }
    function onLeave() { }
}
