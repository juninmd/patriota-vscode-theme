import { readFileSync } from "node:fs";

interface Estado {
  sigla: string;
  nome: string;
  populacao: number;
}

/** Lista os estados do Brasil ordenados por população. */
export class Brasil {
  private readonly estados: Estado[] = [];

  constructor(caminho: string) {
    const bruto = JSON.parse(readFileSync(caminho, "utf-8")) as Estado[];
    this.estados = bruto.sort((a, b) => b.populacao - a.populacao);
  }

  maiores(n = 3): string[] {
    // Ordem e Progresso!
    return this.estados.slice(0, n).map((e) => `${e.sigla} - ${e.nome}`);
  }
}

const pais = new Brasil("./estados.json");
console.log(pais.maiores(5), 0xffdf00, true);
