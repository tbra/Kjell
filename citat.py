import random

fyra_list = [
        'Det finns fyra olika sorters trötthet:\nmattning, domning, avsöndring och utslagning.\nJag är alla fyra samtidigt', 
        'Det finns fyra olika sorters hundar:\nstora, små, boxers och taxar',
        'Det finns fyra sorters sovplatser:\nstenar, rulltrappa, hiss och nalle.\nDen var bäst hittills',
        'Det finns fyra sorters frisyrer:\nhästsvans, helikopterplatta, hockeyfrilla och sidbensfrisyr',
        'Det finns fyra sorters toningar på solglasögon:\nrödtonat, orangetonat, vanligtonat och spegelglastonat',
        'Jag blir galen av det här, jag bara går och rabblar',
        'Det finns fyra olika sorters gosedjur, krokodiler, bamsenallar, rutiga gosedjur och svampnallar'
        ]

cigg_list = [
        'Jag kan röka vad fasen som helst som kommer i min mun',
        'Skulle det komma in ett paket blåbärscigaretter på tobaken, då köper jag det',
        'Kommer det in ett paket med mentol, det är en vanlig smak, då tar jag den för att den är vanlig',
        'Kommer det in cigaretter med russin- och hallonsmak, då tar jag den för att det är kul',
        'Kommer det in någon med turkisk dadlar, ja då tar jag den för att det är lite turkiskt',
        'Kommer det in någon som har spanska flamencocigaretter, som klackar, krack krack krack krack krack, när man röker, ja då röker jag dem för att det klackar',
        'Skulle någon baka in cigaretter i ett bröd, ja då röker jag det brödet, svårare än så är det inte när man är rökare, det är härligt att röka'
        ]

citat_list = [
        'Kul att ni står och röker här, får man ta sig en...kan du fylla på mig här?',
        'Nu tappa jag cigaretten, det är sånt som händer. Cigaretten röker sig själv därnere',
        'Då skulle jag säga att gnejs är som en vattensäng, och granit är som en vanlig säng.',
        'Fyfan vad det ser ut här. Vad är det för monster du har skapat här i köket Birgitta?',
        'Det ser ut som något troll från trollskogen har varit här och haft köttfest',
        'Det här vill jag inte städa upp. Jag skulle vilja ringa en städfirma som gör det här, för det här vill jag inte ta tag i',
        'Fiskmåsar flyger i luften, fiskmåsar och flygplan',
        'Jag är en rökare, jag gillar att röka cigaretter. Det är gott',
        'Nu sitter du!',
        'Jag behöver en ny cigarett, den här är för gammal. Den sular jag ner på gården, nu går jag och tar en hästamacka',
        'Det här är en sån roterare som kör runt saker',
        'Oj, jäklar vad det ser ut här. Jag glömde nog städa av det här, aja skitsamma, det är bara att gå på det igen. Jag tänker inte ge upp den här livsstilen bara för att jag börjat den.',
        'Ja, läget i det här läget är dåligt, det kan jag informera er om',
        'Jag är mikrofob, jag har fobi för mikrofoner',
        'Håret kliar liksom, det är så när man har sömnbrist, det kliar bara',
        'Det är första gången jag, en blå man, från överklassens del av världen, mår så här dåligt',
        'Ta på haka, ta på näsa, ta på mun OCH NU SITTER DU! Du är lösningen på mitt liv och nu sitter du!',
        'Jag röker, det gör jag för att lugna ner mig innan loppet blir av. Så lugn man kan vara innan man blir miljonär, jag känner det där miljonärslugnet',
        'Det är en smart person som jag skrivit den här pärmen. Jag förstår inte ett skvatt, och jag är ändå ett geni',
        'Rinken är ju klubban'
        ]

trav_list =  [
        'Johnny Tractor',
        'Tiffany Tride',
        'Golden Hornline'
        ]

def fyra_sorter():
    return random.choice(fyra_list)

def cigg_citat():
    return random.choice(cigg_list)

def random_citat():
    return random.choice(citat_list)

def random_horse():
    return random.choice(trav_list)