# Teste Prático — Extração, Conferência e Aplicação de Regras em Faturas

Este repositório contém a solução do teste prático para a vaga de Estágio em Tecnologia na Engecomp. O sistema foi desenvolvido em Python 3 utilizando estritamente a biblioteca padrão (`re`, `json`, `pathlib`, `decimal`), respeitando a divisão de responsabilidades em três módulos distintos (Extração, Conferência e Regras).

---

## 📊 Análise dos Dados

**1. Qual unidade consumidora apresentou o maior consumo?**

Com base nas evidências geradas pelo próprio programa, a unidade consumidora com maior consumo foi:
* **Unidade Consumidora (UC):** 55-9087341-2
* **Cliente:** INDUSTRIA METALURGICA BOA VISTA S/A
* **Distribuidora:** CIA LUZ DO VALE
* **Consumo Faturado Original:** 4.780 kWh
* **Consumo Ajustado Final:** 4.827,80 kWh

*Nota explicativa:* O número citado de **4.827,80 kWh** é o valor **ajustado** após a aplicação da regra de Perdas de Transformação do Módulo 3, que calculou um acréscimo de 1% sobre o consumo original de 4.780 kWh por se tratar da distribuidora CIA LUZ DO VALE.

---

## 📝 Questionário

**2. Qual foi o desafio mais marcante que você superou no desenvolvimento de uma feature ou ferramenta?**
No meu histórico na indústria, o desafio mais marcante foi atuar diretamente no comissionamento, calibração e testes de validação de sistemas automatizados industriais junto a engenheiros estrangeiros. Lidar com sistemas complexos que precisavam conversar perfeitamente entre si exigiu muita resiliência, atenção milimétrica aos parâmetros e capacidade de comunicação técnica. Essa vivência prática me deu uma base sólida de como transformar regras operacionais rígidas em processos de software confiáveis.

**3. Quais etapas você costuma seguir quando está incerto sobre um problema?**
Quando enfrento uma incerteza técnica, sigo um fluxo estruturado de engenharia:
1. **Isolamento de Variáveis:** Quebro o problema em partes menores para descobrir exatamente onde a falha acontece (assim como se faz em uma análise de não-conformidade no SAP).
2. **Consulta Técnico-Documental:** Recorro à documentação oficial da linguagem ou ferramenta para entender o comportamento padrão do recurso.
3. **Cenários de Teste:** Crio pequenos testes em ambiente isolado (massa de dados controlada) para validar minhas hipóteses.
4. **Refatoração Segura:** Aplico a solução no código principal apenas após entender completamente a causa raiz do problema.

**4. O que é PEP8?**
A PEP8 é o guia de estilo oficial para o código Python. Ela define regras de formatação (como uso de indentações, limite de caracteres por linha, espaçamentos e padrões de nomes de variáveis e funções) para garantir que o código escrito por desenvolvedores diferentes mantenha um padrão visual limpo, legível e de fácil manutenção por qualquer membro da equipe de engenharia.

**5. No Git, o que são conventional commits?**
Conventional Commits é uma convenção de escrita para mensagens de commit que adiciona um prefixo descritivo e estruturado ao histórico do Git (como `feat:` para novas funcionalidades, `fix:` para correções de bugs, e `docs:` para documentações). Essa prática torna o histórico de desenvolvimento semântico, permitindo que a equipe entenda instantaneamente o propósito de cada alteração sem precisar abrir o código-fonte.
