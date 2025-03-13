# Busca Tabu - Designação Generalizada

Projeto que implementa a Busca Tabu para a alocação de programadores em módulos considerando custos e restrições de carga horária.

## Descrição

O algoritmo lê os dados do arquivo `programadores.txt`, gera uma solução inicial e, a partir dela, explora vizinhos para melhorar a solução usando a meta-heurística Busca Tabu.

## Arquivos

- **programadores.txt**: Dados de entrada contendo:
  - Número de programadores e de módulos.
  - Matriz de custos.
  - Matriz de carga horária.
  - Carga horária disponível para cada programador.
- **busca-tabu_generalizacao.py**: Implementação da Busca Tabu e execução do algoritmo.

## Como Executar

Certifique-se de ter o Python 3 instalado. No terminal, na pasta do projeto, execute:

```bash
python3 busca-tabu_generalizacao.py
```

## Funcionamento

1. Leitura dos dados do arquivo de entrada.
2. Geração de uma solução inicial que minimize o custo.
3. Criação de vizinhos que respeitam as restrições de carga horária.
4. Aplicação da Busca Tabu para otimizar a designação dos módulos aos programadores.

## Licença

Este projeto está licenciado sob a [Unlicense](https://unlicense.org).