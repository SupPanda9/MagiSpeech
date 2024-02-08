[Title/Звание] 

"Магислов"

[Description/Обрисовка] 
Проектът представлява (Top-Down RPG) видеоигра, в която играчите поемат ролята на млад магьосник, използващ говор за управление и взаимодействие със света около него. 
Съчетавайки елементи на фентъзи с иновативни технологии, играта предоставя увлекателно приключение в мистичен свят, битки с различни злодеи и разрешаване на множество
предизвикателства. 

[Functionalities/Надарености] 
1. Двоен начин за управление на герой: 
• Играчът може да управлява героя хибридно чрез клавишите за нагоре, надолу, наляво и надясно, спейс и гласови команди, откривани чрез библиотеки за разпознаване на глас. 
Също така могат да се контролират с глас някои от действията в мини-игрите, но за това после. 
• Играчът може да се контролира изцяло чрез клавиатурата и да настройва желаните бутони за игра. 

2. Възможности на играча/магьосника: 
• Да запраща огнени кълбета и други магии(опционално) към лошите. 
• Да бяга бързичко. 
• Да ходи нормално. 
• Да взима обекти, с които да си служи - тоест да се лекува с плодчета, да взима някакви джаджи и да ги носи на разни места (да, това са side quests) и други такива неща, 
които в зависимост от останалото ми време от планираната времева рамка ще или няма да направя - повече за това в Опционални функционалности.
• Да извършва прости действия, като отваряне на врати, ковчежета и подобни (често срещаният бутон E) 
• Да се лекува и да поема щети. (Много странно звучи на български - това са healing и taking damage) 
• Да качва нива и прогресът му да се пази. • Това, което не може да прави, е да лети, да скача и да плувa. 

3. Изкуствен интелект на противниците: 
• “Изкуствения интелект” е само за подклаждане на интереса. В действителност противниците следват и атакуват играча, използвайки прости стратегии (алгоритми) за сражения, тоест 
изкуствения интелект е силно опростен, но въпреки това доста полезен. Ще има два типа герои: ръкопашни бойци (Melee) и стрелци (Long-range magicians). Ръкопашните бойци следват 
играча и го атакуват отблизо, а стрелците поддържат достатъчно близко разстояние за атакуване и изстрелват снарядите си праволинейно или чрез проследяване на играча, така че 
винаги го удрят. 

4. Множество мини игри: 
Мини игрите може да са част от странични куестове или да бъдат предизвикателство за събиране на ресурс. Те могат или да дадат опит (experience/xp) на играча за качване на нивото му, 
или да му позволят да продължи към следващите стъпки от куеста. 

Видове мини игри:
• Въпросник тип “Стани богат” - въпросите могат да се отговарят както с глас, така и с клавишите/мишка. 
• Memory Match - показва се поредица от емоджита, които при гласово управление имат названия и играчът трябва да запомни правилната подредба и да ги назове едно след друго с посочените 
названия, а при управление с клавиатура/мишка - да ги селектира отново в правилен ред. 
• Sliding Puzzle - пъзел, в който картина е разрязана на 3x3 или 4x4 части в зависимост от трудността и е извадено едно парче. Целта на задачата е да се подреди пъзелът като се плъзгат 
парчетата до правилната наредба. Отново, играта се контролира с глас или клавиатура/мишка. 
• Color Mixing Game - смесване на цветове до получаване на търсения цвят. При гласово управление това се случва чрез назоваване на цветовете. С клавиатурата/мишката е стандартно. 
• Игри, които се случват в отворения свят на играта, включително битки с големи босове (опционално). 
• Всяка мини игра предлага уникален геймплей и възможности за печалба на XP и/или прогресиране. 

5. Система за развитие на нивата: 
• Създаване на система за нива и прогресия за магьосника, базирана на опит от успешно завършени куестове и мини игри. 
• С повишаване на нивото, магьосникът отключва нови умения (евентуално) и текущите му магии стават по-силни. 
• Някои зони на играта ще са забранени до достигане на нужното ниво за отключването им. 

6. Потребителски интерфейс: 
• Менюта за управление на звука, картината, управлението на героя, настройки на клавишите. 
• Healthbar, статистики на героя, ниво, “игрова зона” (playable area)

7. Аудио и графики: 
• Фонова музика, съответстваща на атмосферата на средата. Звукови ефекти за допълнително въздействие при изпращане на огнени топки, срещи с противници и други ключови събития. 
• Готови плочки и герои - използване на предварително създадени графични елементи в стил пиксел арт за герои, места и обекти. (Тук няма нищо python-ско освен самото вмъкване 
на звуците и картинките в играта и тяхната синхронизация с действията). 

8. Опционални (ако всичко мине по мед и масло до тук):
• Локализация - добавяне на български език за диалози и реч 
• Разработка на side quests - тоест самите куестове, а не подготовката за тях, като например носенето на джаджите от магьосника. 
• Карта на светът, в които се играе, с възможност за телепортация. 
• Добавяне на собствен лик към магьосника и персонализации. 

[Milestones/Възлови точки] 
1. Основна структура на играта (12-14 часа): 
• Настройка на основната игрова платформа - включително екран, контроли и изглед. 
• Четене и записване на информация от/във json файлове, работа с файловата система и кодифициране на информацията. 
• Създаване на герой - позиция, движение с клавиши. 
• Създаване на поведение за различните проджектили (магиите, стрели). 
• Управление на нанесените щети и живот (hitboxes). 
• Бутони и менюта. 
• Преход от стая в стая или тоест преминаване между отделните карти.

2. Интеграция на разпознаване на глас (7-8 часа): 
• Интегриране на модул за разпознаване на глас - позволява на играчите да комуникират със света на играта и да извършват специфични действия, посредством своя глас. 
Първоначално на английски, а при останало време и на български. 

3. Система за изкуствен интелект на противници (6-8 часа): 
• Създаване на противниците и задаване на техните характеристики. 
• Създаване на модул за прост и ефективен изкуствен интелект, управляващ действията на противниците чрез алгоритми за следене. 

4. Имплементация на мини игри (10-12 часа): 
• Разработка на отделните модули за всяка мини игра и тяхното свързване с основната. 
• Добавяне на гласови специфики за всяка от игрите. 

5. Система за качване на нива и развитие (5-6 часа): 
• Програмиране на система за управление на опита и нивата, поддържаща прогресията на магьосника. 
• Добавяне на логика за животопроменящи предмети - тези, които дават или отнемат hp. 
• Характеристики на играча и промените, които нанасят на останалите системи. 

6. Интеграция на звуци и картини (5-6 часа): 
• Добавяне на аудио и визуални елементи, съчетаващи фонова музика и ефекти за подобряване на потребителското изживяване. 

7. Дизайн на демо за представяне на всички разработени функционалности (2-3 часа)
• Създаване на демо версия на някаква част от играта с бутони за многократна симулация на едни и същи събития.

[Estimate in man-hours/Времеоценка в човекочасове] 
47-57 часа 

[Usage of technologies/Потребление на технологии] 
1. Pygame: Използван за основното развитие на играта, включително визуализацията и обработката на входни данни. Звуците, картините и менютата също. 

2. SpeechRecognition и PyAudio: Необходими за интегриране на технологията за разпознаване на глас и връзката му с Google Web Speech Api, който е обученият модел за 
разпознаване на думите, изискващ интернет връзка. 

3. Вградени в python библиотеки - random, os, sys, json. 

4. Евентуално Numpy: за изкуствения интелект и различни оптимизации. 

5. Git: За контрол на версиите и лесно управление на проекта. 

6. Готови пиксел арт асети и звуци: Използване на предварително създадени графични елементи в стил пиксел-арт и звукови файлове.

7. Допускам използването на допълнителни библиотеки, за специфични дейности, които може да настъпят в процеса на разработкa. 