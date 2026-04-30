# Sistema RH

Sistema web profissional de gestão de Recursos Humanos voltado para produtores rurais e operações descentralizadas. Construído com Django, arquitetura Clean Architecture e DDD leve, com interface moderna, responsiva e preparada para evolução como produto SaaS.

---

## Visão geral

O sistema atende às necessidades de gestão de pessoas em operações rurais com múltiplos produtores (entidades), fazendas e colaboradores de diferentes vínculos (CLT e diaristas). Cobre o ciclo completo de RH: cadastro de pessoas, lançamento de descontos e parcelamentos, geração de folha mensal, holerites individuais e cálculo de rescisão conforme a CLT brasileira.

---

## Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12, Django 5.0, Django REST Framework |
| Frontend | Django Templates, HTMX 1.9, Alpine.js 3, Tailwind CSS 3.4 |
| Banco de dados | PostgreSQL 16 |
| Cache / Fila | Redis 7, Celery |
| Infraestrutura | Docker, Docker Compose, Nginx |
| Auditoria | django-simple-history |

---

## Arquitetura

O projeto segue Clean Architecture com DDD leve. Cada app Django é organizado em quatro camadas independentes:

```
apps/<modulo>/
├── domain/           # Entidades, regras de negócio, exceções de domínio
├── application/      # Casos de uso, DTOs
├── infrastructure/   # Models Django, repositórios, tasks Celery
└── interfaces/       # Views, Forms, Templates, URLs, Serializers
```

```
core/
├── domain/           # Entidade base, repositório base, value objects
├── application/      # Caso de uso base
└── infrastructure/   # Model base com soft delete, timestamps e auditoria
```

A lógica de negócio fica no `domain` e `application`, isolada do Django. Isso permite testes unitários sem banco de dados, troca de framework sem reescrever regras e adição de API REST sem duplicar lógica.

---

## Módulos implementados

### Cadastros (`apps/employees`)

- **Entidades** — produtores ou grupos econômicos. Base para isolamento multi-tenant futuro.
- **Fazendas** — propriedades vinculadas a cada entidade.
- **Funções** — cargos ocupados pelos colaboradores.
- **Pessoas** — funcionários CLT e diaristas.
  - Dados pessoais, trabalhistas e bancários completos.
  - Filtro dinâmico de fazenda e função por entidade via fetch/HTMX sem reload de página.
  - Inativação com soft delete — histórico preservado permanentemente.
  - Auditoria completa via `django-simple-history`.
  - Tela de detalhe com histórico de descontos e parcelamentos ativos.

### Movimentações

#### Descontos e Ajustes (`apps/attendance`)

- **Ajustes avulsos** — lançamento individual por mês de referência.
  - Tipos: falta, adiantamento, parcela, multa, vale transporte, plano de saúde, hora extra, bônus e outros.
  - Origem rastreada: manual, sistema, módulo de parcelamento, módulo de adiantamentos.
  - Ajustes gerados automaticamente só podem ser cancelados pelo parcelamento de origem.

- **Descontos parcelados** (`DiscountInstallment`) — desconto distribuído em N meses consecutivos.
  - Exemplo: adiantamento de R$ 5.000 em 5x R$ 1.000.
  - `CreateInstallmentUseCase` gera automaticamente um `Adjustment` por mês de referência.
  - Última parcela absorve diferença de arredondamento.
  - Rastreabilidade completa: cada parcela referencia o parcelamento de origem.
  - Tela de detalhe com todas as parcelas e status individual.

#### Adiantamentos (`apps/advances`)

- Registro formal com fluxo de aprovação.
- Status: pendente, aprovado, rejeitado.
- Casos de uso separados para criar, aprovar e rejeitar.

### Relatórios (`apps/payroll`)

#### Fechamento Mensal

- Consolidação por mês e ano, filtrável por entidade.
- Por colaborador: salário base, créditos, descontos e total líquido.
- Totais gerais: bruto, descontos e líquido a pagar.
- Expansão por linha para visualizar lançamentos detalhados do mês.
- Diferencia CLT (salário fixo mensal) e diarista (valor da diária).
- Botão de impressão integrado — exportável como PDF via navegador.

#### Relatório por Rúbrica

- Agrupa todos os lançamentos do mês por tipo de ajuste.
- Subtotal por rúbrica com lista de colaboradores e valores individuais.
- Filtrável por mês, ano e entidade.
- Imprimível diretamente pelo navegador.

#### Holerite Individual

- Seletor de mês, ano e dias trabalhados antes de gerar o documento.
- Para diaristas: calcula automaticamente `dias trabalhados × valor da diária`.
- Para CLT: usa salário mensal fixo.
- Lista proventos, descontos por tipo e total líquido.
- Página formatada para impressão com campo de assinatura.
- Exportável como PDF via `Ctrl+P` no navegador.

#### Rescisão CLT

- Formulário dinâmico com todos os dados necessários para o cálculo.
- Cálculo baseado na CLT vigente com tabela progressiva de INSS 2024.
- Verbas calculadas: saldo de salário, férias vencidas, férias proporcionais, 1/3 constitucional, 13º proporcional, multa FGTS 40%.
- Resultado com memória de cálculo detalhada para auditoria.
- Exportável como PDF via navegador com aviso de uso informativo.

---

## Funcionalidades transversais

| Funcionalidade | Implementação |
|---|---|
| Autenticação | Login nativo Django com controle de sessão |
| Perfis de acesso | admin, RH, gestor, colaborador via `RoleRequiredMixin` |
| Soft delete | Nenhum dado crítico é excluído permanentemente |
| Auditoria | Histórico completo de alterações em todos os modelos |
| Anti duplo submit | Flag `data-submitting` bloqueia reenvio no JavaScript |
| Loading HTMX | Barra de progresso no topo durante requisições assíncronas |
| Mensagens | Sucesso, erro e alerta com auto-fechamento em 5 segundos |
| Responsividade | Sidebar colapsável no mobile, layouts mobile-first |
| Formatação | CPF e CNPJ formatados automaticamente enquanto o usuário digita |
| CSS de impressão | Holerite, rescisão e fechamento mensal exportáveis como PDF via navegador |

---

## Interface e design

Design system construído sobre Tailwind CSS com paleta primary sky blue (`#0284c7`).

| Componente | Descrição |
|---|---|
| `.stat-card` | Cards de resumo numérico no dashboard e relatórios |
| `.table-wrapper` + `.table` | Tabelas com header e bordas padronizados |
| `.form-section` | Seções de formulário com título e espaçamento |
| `.page-header` | Cabeçalho de página com título, subtítulo e ações |
| `.btn`, `.btn-primary`, `.btn-secondary` | Botões consistentes em todos os módulos |
| `.badge-active`, `.badge-danger`, `.badge-info` | Badges de status coloridos |
| `.empty-state` | Estado vazio padronizado com ícone e ação sugerida |
| `.input-field`, `.input-label`, `.input-error` | Campos de formulário uniformes |

---

## Estrutura do projeto

```
.
├── apps/
│   ├── accounts/       # Usuários, autenticação, perfis, dashboard
│   ├── advances/       # Adiantamentos com fluxo de aprovação
│   ├── attendance/     # Descontos avulsos e parcelamentos
│   ├── documents/      # Reservado (sem upload por enquanto)
│   ├── employees/      # Entidades, fazendas, funções, pessoas
│   └── payroll/        # Fechamento mensal, holerite, rúbrica, rescisão
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── celery.py
│   └── urls.py
├── core/               # Bases compartilhadas de Clean Architecture
├── nginx/              # Configuração do Nginx
├── scripts/            # wait_for_db, create_superuser
├── static/
│   ├── css/
│   │   ├── input.css   # Tailwind source com componentes customizados
│   │   ├── output.css  # Compilado pelo Tailwind CLI (não commitado)
│   │   └── custom.css  # Animações, estados HTMX, estilos de impressão
│   └── js/
│       └── main.js     # Proteção duplo submit, formatação CPF/CNPJ, loading HTMX
├── templates/
│   ├── base.html       # Layout base com sidebar colapsável e topbar mobile
│   ├── accounts/       # Login, perfil de usuário
│   ├── attendance/     # Descontos avulsos, parcelamentos
│   ├── dashboard/      # Dashboard principal com métricas e ações rápidas
│   ├── employees/      # Cadastros, detalhe do colaborador
│   ├── partials/       # Mensagens, paginação, confirmação de exclusão
│   └── payroll/        # Fechamento, holerite, seletor, rúbrica, rescisão
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── tailwind.config.js
└── tailwindcss         # Binário standalone do Tailwind CLI (sem Node.js)
```

---

## Configuração e execução

### Pré-requisitos

- Docker e Docker Compose instalados.
- Binário `tailwindcss` na raiz do projeto (Tailwind CLI standalone, não requer Node.js).

### Subir o ambiente de desenvolvimento

```bash
# Subir todos os serviços
docker compose up -d

# Aplicar migrações
docker compose exec web python manage.py migrate

# Criar superusuário
docker compose exec web python manage.py createsuperuser

# Compilar CSS (obrigatório na primeira vez e após mudanças nos templates)
./tailwindcss -i ./static/css/input.css -o ./static/css/output.css
```

### Comandos via Makefile

```bash
make up              # Subir containers
make down            # Derrubar containers
make restart         # Reiniciar containers
make migrate         # Aplicar migrações
make makemigrations  # Gerar migrações pendentes
make shell           # Shell Django interativo
make logs            # Logs do serviço web
make logs-worker     # Logs do Celery worker
make css-watch       # Tailwind em modo watch (rebuild automático)
make css-build       # Tailwind build minificado para produção
make db-shell        # Shell do PostgreSQL
```

### URLs do sistema

| URL | Módulo |
|---|---|
| `/` | Dashboard |
| `/funcionarios/` | Lista de colaboradores |
| `/funcionarios/novo/` | Cadastrar colaborador |
| `/funcionarios/<pk>/` | Detalhe do colaborador |
| `/funcionarios/<pk>/editar/` | Editar colaborador |
| `/funcionarios/entidades/` | Gerenciar entidades |
| `/funcionarios/fazendas/` | Gerenciar fazendas |
| `/funcionarios/funcoes/` | Gerenciar funções |
| `/frequencia/` | Descontos e ajustes do mês |
| `/frequencia/novo/` | Registrar desconto avulso |
| `/frequencia/parcelamentos/` | Lista de parcelamentos |
| `/frequencia/parcelamentos/novo/` | Criar desconto parcelado |
| `/frequencia/parcelamentos/<pk>/` | Detalhe do parcelamento |
| `/adiantamentos/` | Adiantamentos |
| `/folha/` | Fechamento mensal com impressão |
| `/folha/rubricas/` | Relatório por rúbrica |
| `/folha/holerite/<pk>/selecionar/` | Seletor de mês e dias para holerite |
| `/folha/holerite/<pk>/` | Holerite individual imprimível |
| `/folha/rescisao/` | Cálculo de rescisão CLT |

---

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste:

```env
SECRET_KEY=sua-chave-secreta-longa-e-aleatoria
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development

DB_NAME=rh_db
DB_USER=rh_user
DB_PASSWORD=senha_segura
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
```

---

## Fluxo de trabalho típico

```
1. Cadastrar entidades (produtores/grupos)
2. Cadastrar fazendas vinculadas a cada entidade
3. Cadastrar funções (cargos)
4. Cadastrar colaboradores (CLT ou diarista)
        ↓
5. Durante o mês:
   - Lançar descontos avulsos (faltas, multas etc.)
   - Criar parcelamentos para adiantamentos
        ↓
6. Fechamento do mês:
   - Acessar /folha/ e filtrar por entidade/mês
   - Revisar salários, descontos e líquidos
   - Imprimir relatório de fechamento
        ↓
7. Holerites:
   - Acessar detalhe de cada colaborador
   - Selecionar mês e dias trabalhados (diaristas)
   - Imprimir holerite para assinatura
        ↓
8. Demissão:
   - Acessar /folha/rescisao/
   - Preencher dados e calcular verbas
   - Imprimir rescisão para assinatura
```

---

## Decisões técnicas

**Clean Architecture + DDD leve**
As regras ficam no `domain` e `application`, desacopladas do Django. Permite adicionar API REST, trocar banco de dados ou extrair microserviços sem reescrever a lógica de negócio. O custo inicial é compensado pela facilidade de evolução a longo prazo.

**Soft delete obrigatório**
Dados de RH são sujeitos a fiscalização trabalhista. Colaboradores, descontos e folhas jamais devem ser removidos do histórico. O soft delete garante rastreabilidade completa sem poluir as listagens ativas do sistema.

**HTMX em vez de SPA**
O cliente opera em ambientes rurais com conexão instável. HTMX entrega interatividade sem bundle JavaScript pesado, funciona em conexões 2G/3G e dispositivos de entrada. Curva de aprendizado zero para quem já conhece HTML.

**Tailwind CLI standalone**
Elimina Node.js do ambiente de desenvolvimento e do container Docker. O binário é suficiente para gerar o CSS em desenvolvimento e produção, simplificando o setup.

**Celery + Redis desde o início**
A infraestrutura assíncrona está pronta para notificações automáticas, geração de PDFs em background e rotinas de fechamento — sem mudança de arquitetura quando o volume crescer.

**PDF via CSS de impressão**
Elimina dependências pesadas como WeasyPrint ou Puppeteer. O usuário usa `Ctrl+P` no navegador e salva como PDF nativo. Zero configuração, compatível com qualquer dispositivo e sistema operacional.

---

## Regras de negócio críticas

- A folha fecha no último dia de cada mês.
- Todo lançamento deve ter mês de referência explícito.
- Ajustes gerados por parcelamentos não podem ser excluídos diretamente.
- Nenhum dado histórico é excluído — soft delete em todos os modelos críticos.
- CLT e diaristas têm regras de cálculo distintas na folha e no holerite.
- Cada entidade é tratada como empresa independente — base para multi-tenant.
- O cálculo de rescisão é informativo e deve ser validado por contador.

---

## Roadmap

### Implementado

- [x] Cadastros completos — entidades, fazendas, funções, pessoas (CLT e diarista)
- [x] Filtro dinâmico de fazenda e função por entidade via HTMX
- [x] Tela de detalhe do colaborador com histórico financeiro
- [x] Descontos avulsos por mês de referência
- [x] Descontos parcelados com geração automática de parcelas mensais
- [x] Adiantamentos com fluxo de aprovação
- [x] Fechamento mensal com expansão por linha e impressão via navegador
- [x] Relatório por rúbrica com agrupamento por tipo de ajuste
- [x] Holerite individual com seletor de mês e dias trabalhados
- [x] Holerite diferenciado para CLT e diarista
- [x] Rescisão CLT com formulário dinâmico, cálculo e PDF
- [x] Soft delete e auditoria completa em todos os módulos
- [x] Interface responsiva mobile-first com sidebar colapsável
- [x] Proteção contra duplo submit

### Curto prazo

- [ ] Módulo de férias — período aquisitivo, gozo e saldo por colaborador
- [ ] Holerite com INSS calculado para CLT — desconto estimado no recibo
- [ ] Tela de gestão de usuários pela interface do sistema
- [ ] Filtros avançados na lista de colaboradores (fazenda, função, status)

### Médio prazo

- [ ] Notificações via Celery — parcelamentos nos últimos meses, férias a vencer
- [ ] Exportação do fechamento mensal em Excel via openpyxl
- [ ] Log de auditoria visível na interface — quem alterou o quê e quando
- [ ] Relatório de admissões e demissões por período
- [ ] Tela de histórico financeiro anual por colaborador

### Longo prazo — evolução para SaaS

- [ ] Multi-tenant completo — isolamento por entidade com planos e billing
- [ ] API REST completa com DRF — preparação para aplicativo mobile
- [ ] Autenticação via JWT para a API
- [ ] Integração com eSocial — eventos S-2200 e S-2299
- [ ] Painel de administração SaaS — gestão de clientes, planos e faturamento
- [ ] Aplicativo mobile — acesso offline, push notifications, assinatura digital de holerites
- [ ] Integração com sistemas contábeis externos

---

## Licença

Uso interno. Todos os direitos reservados.
