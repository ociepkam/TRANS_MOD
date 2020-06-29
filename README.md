# TRANS
Zadanie do badania Ś

Pokazuje się pionowo 2, 3, 4, lub 5 (k) par w postaci X>Y lub X<Y, gdzie X i Y to figury geometryczne spośród zestawu 7 figur, a „<” albo „>” to znak relacji. Użytych figur w danym itemie testu jest zawsze k+2. Litery i znak relacji są wybierane do pary losowo, z ograniczeniami:
dana para symboli może wystąpić tylko raz (tzn. jeśli ∆ i □ zostało sparowane, to nie może być 2 raz) [to ograniczenie powoduje, ze dla k = 2 obie pary zawierają 4 rozłączne figury),
każdy znak relacji został użyty przynajmniej 1 raz (czyli przy k = 2 użyte 1 raz są oba znaki relacji).

W odróżnieniu od zwykłego transrela, w transie figurami nie musi rządzić żaden liniowy porządek.

Pod parami pokazują się zawsze 4 inne pary, z których 2 pary odzwierciedlają poprawnie odwrócone relacyjnie pary (tzn. para ∆>□ zostaje odwrócona w □<∆ - odwraca się zarówno kolejność figur oraz znak relacji), a pozostałe dwie pary albo mają odwrócone figury ale nie znak relacji (□>∆), albo jest odwrócony znak ale nie symbole (∆<□). 

Opcje błędne generowane są losowo (tzn. może pojawić się dowolna dopuszczalna kombinacja odwróconych figur (bez odwrócenia znaku) albo odwróconych znaków (bez odwrócenia figur) dla dowolnych par.

Zadanie polega na kliknięciu myszką na poprawne pary (dwa kliknięcia, po jednym na każdej poprawnej parze). Kliknięcie na przynajmniej jednej niepoprawnej parze, albo brak dwóch kliknięć w limicie czasu oznacza błąd.

Feedback polega na oznaczeniu (np. zieloną ramką) poprawnych odpowiedzi.

Odpowiedzi udzielane są myszką.

Trening z feedbackiem “w trialu” - znaczy to, że item nie znika po udzieleniu odpowiedzi, a informacja czy odpowiedź była poprawna czy nie, wyświetlana jest u dołu ekranu pod itemem. Oprócz tej informacji, poprawne rozwiązanie zostaje oznaczona na itemie (w każdym zadaniu wygląda to nieco inaczej). Feedback znika po kliknięciu myszką (a może jakiś inny sposób?)

Trening jest warunkowy - warunkiem przejścia jest osiągnięcie określonej poprawności w treningu (parametr do ustawienia w configu). Jeśli wymagana poprawność nie zostaje osiągnięta, pojawia się odpowiednia informacja i trening rozpoczyna się ponownie - aż do skutku.

Tak jak ostatnio, istnieje ograniczenie czasowe na trial, a na określoną ilość czasu przed jego osiągnięciem wyświetlona zostaje ikonka zegarka.

