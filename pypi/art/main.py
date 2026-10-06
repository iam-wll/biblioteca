from art import art, artError


art_1 = art("cafe")
print(art_1)

art_2 = art("mulher", number=2)
print(art_2)

print(art("cafe", number=3, space=5))
print(art("mulher"))
print(art("aleatorio"))

try:
    art(22, number=1)
except artError as error:
    print(f"Erro esperado: {error}")
