"""
ArthaMind AI — Financial Learning Hub Module
==============================================
Structured financial education content for Indian citizens.
Each topic includes explanation, benefits, examples, and key points.
"""

from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
#  DATA MODEL
# ═══════════════════════════════════════════════════════════════

@dataclass
class LearningTopic:
    """A financial learning module."""
    icon: str
    title: str
    subtitle: str
    content: str
    category: str


# ═══════════════════════════════════════════════════════════════
#  LEARNING CONTENT
# ═══════════════════════════════════════════════════════════════

LEARNING_TOPICS: list[LearningTopic] = [

    # ── GST ──────────────────────────────────────────────────
    LearningTopic(
        icon="🧾",
        title="GST — Goods and Services Tax",
        subtitle="Understanding India's unified indirect tax",
        category="Taxation",
        content="""
## What is GST?

GST (Goods and Services Tax) is a **comprehensive indirect tax** on the supply of goods and services in India. Launched on **July 1, 2017**, it replaced multiple taxes like VAT, excise duty, and service tax, creating **"One Nation, One Tax"**.

## GST Rate Slabs

| Rate | Category | Examples |
|------|----------|----------|
| **0%** | Essentials | Fresh food, milk, eggs, bread |
| **5%** | Basic needs | Sugar, tea, packaged food, medicines |
| **12%** | Standard | Butter, ghee, phones, processed food |
| **18%** | Most items | Biscuits, IT services, restaurants (AC) |
| **28%** | Luxury | Cars, ACs, tobacco, aerated drinks |

## Key Benefits
- ✅ **Simplified taxation** — one tax replaces 17+ indirect taxes
- ✅ **Input Tax Credit** — avoid cascading effect (tax on tax)
- ✅ **Unified market** — seamless inter-state trade
- ✅ **Transparency** — digital invoicing and filing

## Example
You buy a laptop for ₹50,000 (base) in the same state:
- GST @ 18% = ₹9,000
- CGST (9%) = ₹4,500 | SGST (9%) = ₹4,500
- **Total: ₹59,000**

## Important Points
- 📌 Registration mandatory if turnover > ₹40 lakh (₹20 lakh for services)
- 📌 GSTIN is a 15-digit unique number
- 📌 File GSTR-3B monthly by the 20th
- 📌 E-way bill needed for goods movement above ₹50,000
- 📌 Composition scheme available for small businesses (turnover up to ₹1.5 crore)
""",
    ),

    # ── Income Tax ───────────────────────────────────────────
    LearningTopic(
        icon="💰",
        title="Income Tax in India",
        subtitle="Old regime vs New regime — what's best for you?",
        category="Taxation",
        content="""
## What is Income Tax?

Income Tax is a **direct tax** levied by the Government of India on the income earned by individuals, HUFs, companies, and other entities. It is governed by the **Income Tax Act, 1961**.

## New Regime (Default from FY 2023-24)

| Income Slab | Tax Rate |
|-------------|----------|
| Up to ₹4,00,000 | Nil |
| ₹4,00,001 – ₹8,00,000 | 5% |
| ₹8,00,001 – ₹12,00,000 | 10% |
| ₹12,00,001 – ₹16,00,000 | 15% |
| ₹16,00,001 – ₹20,00,000 | 20% |
| ₹20,00,001 – ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

*Standard deduction of ₹75,000. Rebate u/s 87A for income up to ₹12 lakh (effective zero tax up to ₹12.75 lakh for salaried).*

## Key Benefits of New Regime
- ✅ Lower rates and more slabs
- ✅ Simpler — no deductions to track
- ✅ Standard deduction of ₹75,000

## When to Choose Old Regime
Choose Old Regime if your total deductions (80C, 80D, HRA, LTA) exceed **~₹3.75 lakh**.

## Example
Salaried individual earning ₹15,00,000 under New Regime:
- Standard deduction: ₹75,000 → Taxable = ₹14,25,000
- Tax = 0 + 20,000 + 40,000 + 33,750 = **₹93,750**
- With 4% cess = **₹97,500**

## Important Points
- 📌 ITR filing deadline: July 31 each year
- 📌 Advance tax if liability > ₹10,000
- 📌 Form 16 from employer is key document
- 📌 Check Form 26AS for TDS credits
""",
    ),

    # ── Mutual Funds ─────────────────────────────────────────
    LearningTopic(
        icon="📊",
        title="Mutual Funds & SIP",
        subtitle="Start investing with as little as ₹100/month",
        category="Investment",
        content="""
## What are Mutual Funds?

Mutual funds pool money from multiple investors to invest in stocks, bonds, and other securities, managed by professional fund managers regulated by **SEBI**.

## Types of Mutual Funds

| Type | Risk | Best For |
|------|------|----------|
| **Equity (Large Cap)** | Medium-High | Stable long-term growth |
| **Equity (Mid/Small Cap)** | High | Aggressive growth |
| **Debt Funds** | Low | Capital preservation |
| **Hybrid/Balanced** | Medium | Balanced approach |
| **ELSS** | High | Tax saving (Sec 80C) |
| **Index Funds** | Medium | Low-cost passive investing |

## What is SIP?

**Systematic Investment Plan (SIP)** lets you invest a fixed amount regularly. It's the best way for beginners to start.

## Key Benefits
- ✅ **Start small** — as low as ₹100/month
- ✅ **Rupee cost averaging** — reduces timing risk
- ✅ **Power of compounding** — ₹5,000/month @ 12% for 20 years = ₹~50 lakh
- ✅ **Professional management** — experts manage your money
- ✅ **Tax savings** — ELSS gives 80C deduction up to ₹1.5 lakh

## Example: Power of SIP
| Monthly SIP | Years | @12% Return | Total Invested | Corpus |
|------------|-------|-------------|----------------|--------|
| ₹5,000 | 10 | 12% | ₹6,00,000 | ₹11,61,695 |
| ₹5,000 | 20 | 12% | ₹12,00,000 | ₹49,95,740 |
| ₹10,000 | 30 | 12% | ₹36,00,000 | ₹3,52,99,138 |

## Important Points
- 📌 Choose **Direct plans** over Regular (lower expense ratio)
- 📌 KYC is mandatory (do e-KYC via CAMS/KFintech)
- 📌 LTCG tax: 12.5% above ₹1.25 lakh (equity funds)
- 📌 Don't stop SIP during market crashes — that's when you buy cheap!
- 📌 Review portfolio annually, not daily
""",
    ),

    # ── PPF ──────────────────────────────────────────────────
    LearningTopic(
        icon="🏦",
        title="PPF — Public Provident Fund",
        subtitle="Government-backed tax-free savings for 15 years",
        category="Savings",
        content="""
## What is PPF?

PPF is a **government-backed savings scheme** offering guaranteed returns and complete tax exemption (EEE status — Exempt at investment, interest, and maturity).

## Key Features

| Feature | Detail |
|---------|--------|
| **Interest Rate** | 7.1% p.a. (reviewed quarterly by GoI) |
| **Lock-in** | 15 years (extendable in 5-year blocks) |
| **Min Investment** | ₹500/year |
| **Max Investment** | ₹1,50,000/year |
| **Tax Benefit** | Section 80C + Interest tax-free + Maturity tax-free |
| **Where to Open** | Post office, SBI, HDFC, ICICI, and other nationalized banks |

## Key Benefits
- ✅ **100% safe** — sovereign guarantee by Government of India
- ✅ **Tax-free returns** — EEE (Exempt-Exempt-Exempt)
- ✅ **Section 80C** — up to ₹1.5 lakh deduction
- ✅ **Loan facility** — from 3rd to 6th year
- ✅ **Partial withdrawal** — from 7th year onwards

## Example
Invest ₹1,50,000/year for 15 years @ 7.1%:
- Total invested: ₹22,50,000
- Maturity value: ₹~40,68,209
- Interest earned: ₹~18,18,209 (completely tax-free!)

## Important Points
- 📌 Only **one PPF account** per person (not one per bank)
- 📌 Deposit at least ₹500/year to keep it active
- 📌 Deposit before **5th of the month** for interest calculation
- 📌 Cannot be attached by courts — fully protected
- 📌 NRIs cannot open new PPF accounts
""",
    ),

    # ── NPS ──────────────────────────────────────────────────
    LearningTopic(
        icon="👴",
        title="NPS — National Pension System",
        subtitle="Build your retirement corpus with additional tax benefits",
        category="Retirement",
        content="""
## What is NPS?

NPS is a **voluntary retirement savings scheme** regulated by PFRDA. It offers market-linked returns and additional tax benefits beyond Section 80C.

## Key Features

| Feature | Detail |
|---------|--------|
| **Regulator** | PFRDA |
| **Min Contribution** | ₹500/year (Tier-I) |
| **Tax Benefit (80CCD(1))** | Up to ₹1.5 lakh (within 80C) |
| **Extra Tax Benefit (80CCD(1B))** | Additional ₹50,000 (exclusive!) |
| **At Maturity** | 60% lump sum (tax-free) + 40% annuity |
| **Lock-in** | Until age 60 |

## Asset Classes

| Class | Type | Risk |
|-------|------|------|
| **E** | Equity | High |
| **C** | Corporate Bonds | Medium |
| **G** | Government Securities | Low |
| **A** | Alternative Investments | Medium-High |

## Key Benefits
- ✅ **Extra ₹50,000 tax deduction** — over and above 80C
- ✅ **Market-linked returns** — potential for higher returns than PPF
- ✅ **Low charges** — one of the lowest expense ratios
- ✅ **Portable** — works across jobs and states
- ✅ **60% tax-free withdrawal** at maturity

## Example
Monthly NPS contribution of ₹5,000 for 30 years @ 10% return:
- Total invested: ₹18,00,000
- Estimated corpus: ₹1,13,96,627
- Tax saved annually: ₹15,600 (at 30% + cess, on ₹50,000 u/s 80CCD(1B))

## Important Points
- 📌 Open account via eNPS portal or Point of Presence (PoP)
- 📌 Two tiers: Tier-I (retirement, restricted withdrawal) and Tier-II (flexible)
- 📌 **Auto choice** — automatically shifts from equity to bonds as you age
- 📌 Partial withdrawal allowed (up to 25% of own contributions) for specific purposes
- 📌 Employer contributions deductible u/s 80CCD(2) — no upper limit cap!
""",
    ),

    # ── Insurance ────────────────────────────────────────────
    LearningTopic(
        icon="🛡️",
        title="Insurance — Term & Health",
        subtitle="Protect yourself and your family from financial shocks",
        category="Protection",
        content="""
## Why Insurance?

Insurance is a **risk transfer mechanism** — you pay a small premium to protect against large financial losses. The two most important types for every Indian:

## 1. Term Life Insurance

| Feature | Detail |
|---------|--------|
| **What** | Pure protection — pays sum assured on death |
| **Premium** | Very low (₹500-800/month for ₹1 crore cover at age 30) |
| **Ideal Cover** | 10-15× annual income |
| **Tax Benefit** | Premium under 80C, claim tax-free u/s 10(10D) |

### How much cover do you need?
- Annual income × 15 = Ideal cover
- ₹8,00,000 income → ₹1.2 crore cover

## 2. Health Insurance

| Feature | Detail |
|---------|--------|
| **What** | Covers hospitalization expenses |
| **Types** | Individual, Family Floater, Top-up, Super Top-up |
| **Tax Benefit** | Section 80D (₹25,000 self; ₹25,000 parents; ₹50,000 for senior citizens) |
| **Ideal Cover** | ₹10-25 lakh (₹50 lakh+ in metro cities) |

## Key Benefits
- ✅ **Financial protection** for family in case of death or illness
- ✅ **Tax savings** — 80C (life) and 80D (health)
- ✅ **Cashless treatment** at network hospitals
- ✅ **No-claim bonus** — sum insured increases every claim-free year

## Important Points
- 📌 **Buy term insurance EARLY** — premiums are lowest when young
- 📌 **Never mix insurance with investment** — avoid ULIPs and endowment plans
- 📌 **Declare all medical history** honestly — prevents claim rejection
- 📌 **Check waiting period** — pre-existing diseases typically have 2-4 year wait
- 📌 **Compare plans** on Policybazaar or InsuranceDekho before buying
""",
    ),

    # ── Budget Planning ──────────────────────────────────────
    LearningTopic(
        icon="📋",
        title="Budget Planning — 50-30-20 Rule",
        subtitle="Master your money with a simple budgeting framework",
        category="Planning",
        content="""
## The 50-30-20 Rule

The simplest and most effective budgeting framework, popularized by Elizabeth Warren:

| Category | % of Income | What's Included |
|----------|-------------|-----------------|
| 🔵 **Needs** | 50% | Rent, food, utilities, EMIs, insurance, transport |
| 🟡 **Wants** | 30% | Entertainment, dining out, shopping, travel, subscriptions |
| 🟢 **Savings** | 20% | SIP, PPF, FD, NPS, emergency fund |

## Example (₹50,000 income)

| Category | Amount |
|----------|--------|
| Needs (50%) | ₹25,000 |
| Wants (30%) | ₹15,000 |
| Savings (20%) | ₹10,000 |

## Key Benefits
- ✅ **Simple** — only 3 categories to manage
- ✅ **Balanced** — covers needs, lifestyle, and future
- ✅ **Guilt-free spending** — 30% for wants is planned!
- ✅ **Automated savings** — set up SIP for the 20%

## Tips for Successful Budgeting
- 📌 **Track expenses** for 1 month before starting
- 📌 **Automate savings** — SIP on salary day (1st or 5th)
- 📌 **Pay yourself first** — save before spending
- 📌 **Use apps** — Walnut, Money Manager, or Excel
- 📌 **Review monthly** — adjust as income changes
- 📌 **Emergency fund first** — 6 months expenses before investing
""",
    ),

    # ── Credit Score ─────────────────────────────────────────
    LearningTopic(
        icon="💳",
        title="Credit Score — CIBIL Guide",
        subtitle="Understanding and improving your creditworthiness",
        category="Credit",
        content="""
## What is CIBIL Score?

CIBIL Score (by TransUnion CIBIL) is a 3-digit number (300-900) that represents your **creditworthiness**. Banks and lenders check this before approving loans or credit cards.

## Score Ranges

| Score | Rating | Impact |
|-------|--------|--------|
| **800-900** | 🟢 Excellent | Best rates, instant approval |
| **750-799** | 🟢 Good | Easy approval, good rates |
| **700-749** | 🟡 Fair | Approval likely, higher rates |
| **650-699** | 🟠 Below Average | May need collateral |
| **Below 650** | 🔴 Poor | Likely rejection |

## What Affects Your Score?

| Factor | Weight | Impact |
|--------|--------|--------|
| **Payment History** | 35% | Biggest factor — always pay on time! |
| **Credit Utilization** | 30% | Keep below 30% of limit |
| **Credit History Length** | 15% | Longer is better |
| **Credit Mix** | 10% | Mix of secured + unsecured |
| **New Credit** | 10% | Too many inquiries hurt |

## How to Improve Your Score
1. 📌 **Pay EMIs and bills ON TIME** — most important factor
2. 📌 **Keep credit card utilization below 30%** (₹30K spend on ₹1L limit)
3. 📌 **Don't close old credit cards** — they add to history length
4. 📌 **Don't apply for multiple loans** at once — hard inquiries reduce score
5. 📌 **Check report regularly** — dispute errors with CIBIL
6. 📌 **Maintain a mix** — one credit card + one loan is ideal

## How to Check (Free!)
- CIBIL website (1 free per year)
- CRED app, Paytm, PhonePe (free monthly updates)
- Bank apps (HDFC, SBI YONO)
""",
    ),

    # ── Emergency Fund ───────────────────────────────────────
    LearningTopic(
        icon="🆘",
        title="Emergency Fund",
        subtitle="Your financial safety net for life's surprises",
        category="Planning",
        content="""
## What is an Emergency Fund?

An emergency fund is a **readily accessible reserve of money** to cover unexpected financial needs — job loss, medical emergency, car repair, or home issues.

## How Much Do You Need?

| Situation | Recommended Fund |
|-----------|-----------------|
| Dual income, no dependents | 3-6 months of expenses |
| Single earner, family | 6-9 months of expenses |
| Self-employed / Freelancer | 9-12 months of expenses |
| Nearing retirement | 12+ months of expenses |

## Example
Monthly expenses: ₹40,000
Emergency fund target: ₹40,000 × 6 = **₹2,40,000**

## Where to Park Emergency Fund?

| Option | Liquidity | Returns | Best For |
|--------|-----------|---------|----------|
| **Savings Account** | Instant | 2.5-4% | First ₹50,000 |
| **Liquid Mutual Fund** | T+1 day | 5-7% | Bulk of emergency fund |
| **Sweep-in FD** | Instant | 5-7% | Hybrid approach |
| **Short-term FD** | 1-day break | 6-7% | Partial parking |

## Key Benefits
- ✅ **Peace of mind** — no panic during crises
- ✅ **Avoid debt** — don't need personal loans or credit card debt
- ✅ **Protect investments** — don't break SIPs or FDs
- ✅ **Handle job transitions** — time to find the right job

## Building Your Emergency Fund
1. 📌 **Start now** — even ₹2,000/month adds up
2. 📌 **Automate** — set standing instruction on salary day
3. 📌 **Keep it separate** — different account from spending
4. 📌 **Don't invest in equity** — emergency fund must be safe and liquid
5. 📌 **Replenish immediately** after using it
""",
    ),

    # ── UPI & Digital Payments ───────────────────────────────
    LearningTopic(
        icon="📱",
        title="UPI & Digital Payments",
        subtitle="India's digital payment revolution explained",
        category="Banking",
        content="""
## What is UPI?

UPI (Unified Payments Interface) is a **real-time payment system** developed by NPCI (National Payments Corporation of India). It allows instant money transfer using a virtual address (VPA) like `name@bank`.

## Key Features

| Feature | Detail |
|---------|--------|
| **Speed** | Instant (real-time, 24/7) |
| **Cost** | Free for consumers |
| **Limit** | ₹1-2 lakh per transaction (varies by bank) |
| **Apps** | BHIM, PhonePe, Google Pay, Paytm, Amazon Pay |

## UPI Ecosystem

| Product | Purpose | Who Uses |
|---------|---------|----------|
| **UPI** | Regular payments | Everyone with smartphone |
| **UPI Lite** | Small payments (≤₹500) | Quick offline payments |
| **UPI 123PAY** | Feature phone payments | Non-smartphone users |
| **UPI Autopay** | Recurring payments | SIP, bills, subscriptions |
| **UPI International** | Cross-border payments | Travelers abroad |

## Safety Tips 🔒
1. 📌 **Never share UPI PIN** — it's like your ATM PIN
2. 📌 **Don't scan QR to receive** — QR codes are for paying, not receiving!
3. 📌 **Verify before sending** — check name and amount carefully
4. 📌 **Use app lock** — fingerprint or PIN on UPI apps
5. 📌 **Report fraud immediately** — call bank + report on cybercrime.gov.in
6. 📌 **Don't click random links** — fraudsters send fake payment requests

## Fun Facts
- 🇮🇳 India processes **14+ billion UPI transactions/month** (2025)
- 💰 UPI handles over **₹20 lakh crore/month** in value
- 🌍 UPI is now accepted in **7+ countries** (Singapore, UAE, France, Sri Lanka, etc.)
""",
    ),

    # ── Real Estate & Home Loans ─────────────────────────────
    LearningTopic(
        icon="🏠",
        title="Home Loans & Real Estate",
        subtitle="Navigate your biggest financial decision wisely",
        category="Loans",
        content="""
## Home Loan Basics

A home loan is a **secured loan** where the property serves as collateral. Interest rates can be **fixed** or **floating** (linked to repo rate).

## Key Parameters

| Parameter | Typical Range |
|-----------|--------------|
| **Interest Rate** | 8% – 9.5% p.a. (floating) |
| **Tenure** | 5 – 30 years |
| **LTV Ratio** | Up to 80-90% of property value |
| **Processing Fee** | 0.25% – 1% of loan amount |

## Tax Benefits on Home Loan

| Section | Deduction | On |
|---------|-----------|-----|
| **Section 80C** | Up to ₹1,50,000 | Principal repayment |
| **Section 24(b)** | Up to ₹2,00,000 | Interest payment (self-occupied) |
| **Section 80EEA** | Up to ₹1,50,000 | Additional interest (first-time buyers, if eligible) |

## EMI Example
- Loan: ₹50,00,000 | Rate: 8.5% | Tenure: 20 years
- **Monthly EMI: ₹43,391**
- Total Payment: ₹1,04,13,784
- Total Interest: ₹54,13,784

## Important Points
- 📌 **Compare rates** across banks — even 0.25% matters over 20 years
- 📌 **Prepay when possible** — even ₹50,000 extra/year saves lakhs in interest
- 📌 **Check RERA registration** — mandatory for under-construction properties
- 📌 **Keep EMI ≤ 40% of income** — healthy debt ratio
- 📌 **Get pre-approved** before property hunting — know your budget
- 📌 **Stamp duty & registration** — additional 5-8% of property value
""",
    ),
]


# ═══════════════════════════════════════════════════════════════
#  LEARNING HUB CLASS
# ═══════════════════════════════════════════════════════════════

class FinancialLearningHub:
    """Manages and serves financial education content."""

    def __init__(self):
        self.topics = LEARNING_TOPICS

    def get_all_topics(self) -> list[LearningTopic]:
        """Return all available learning topics."""
        return self.topics

    def get_topic_by_title(self, title: str) -> LearningTopic | None:
        """Find a topic by its exact title.

        Args:
            title: Topic title to search for.

        Returns:
            Matching LearningTopic or None.
        """
        for topic in self.topics:
            if topic.title == title:
                return topic
        return None

    def get_topics_by_category(self, category: str) -> list[LearningTopic]:
        """Get all topics in a category.

        Args:
            category: Category name (e.g. 'Taxation', 'Investment').

        Returns:
            List of matching topics.
        """
        return [t for t in self.topics if t.category.lower() == category.lower()]

    def get_categories(self) -> list[str]:
        """Return all unique categories."""
        return sorted(set(t.category for t in self.topics))

    def format_topic_card(self, topic: LearningTopic) -> str:
        """Format a topic as a markdown card for display.

        Args:
            topic: LearningTopic to format.

        Returns:
            Markdown-formatted topic card.
        """
        return (
            f"## {topic.icon} {topic.title}\n\n"
            f"*{topic.subtitle}*\n\n"
            f"**Category:** {topic.category}\n\n"
            f"---\n\n"
            f"{topic.content.strip()}"
        )

    def get_topic_summary_cards(self) -> str:
        """Generate a summary grid of all topics for the learning hub main page.

        Returns:
            Markdown-formatted summary of all topics.
        """
        lines = ["# 📚 Financial Learning Hub\n"]
        lines.append("*Master personal finance with easy-to-understand guides tailored for Indian citizens.*\n\n")
        lines.append("| # | Topic | Category | Description |")
        lines.append("|---|-------|----------|-------------|")
        for i, topic in enumerate(self.topics, 1):
            lines.append(f"| {i} | {topic.icon} {topic.title} | {topic.category} | {topic.subtitle} |")
        lines.append("\n\n*Select a topic below to learn more ↓*")
        return "\n".join(lines)


# ── Module-level singleton ──────────────────────────────────
learning_hub = FinancialLearningHub()
