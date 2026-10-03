from dataclasses import dataclass

@dataclass
class Dev:
    nome: str
    linguagem: str = "Python"

    def saudar(self) -> str:
        return f"Salve, {self.nome}! 🇧🇷"

if __name__ == "__main__":
    print(Dev("Junin").saudar())
