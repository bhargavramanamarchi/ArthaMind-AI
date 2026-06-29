"""
ArthaMind AI — Financial Calculators Module
=============================================
Pure financial calculation functions with no external API dependencies.
Each function returns structured results suitable for display.
"""

from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════
#  DATA CLASSES
# ═══════════════════════════════════════════════════════════════

@dataclass
class EMIResult:
    """Result of an EMI calculation."""
    principal: float
    annual_rate: float
    tenure_years: int
    monthly_emi: float
    total_payment: float
    total_interest: float
    yearly_breakdown: list[dict[str, float]] = field(default_factory=list)


@dataclass
class SIPResult:
    """Result of a SIP calculation."""
    monthly_investment: float
    annual_return_rate: float
    tenure_years: int
    total_invested: float
    future_value: float
    wealth_gained: float
    yearly_breakdown: list[dict[str, float]] = field(default_factory=list)


@dataclass
class CompoundInterestResult:
    """Result of a compound interest calculation."""
    principal: float
    annual_rate: float
    tenure_years: int
    compounding_frequency: str
    final_amount: float
    total_interest: float
    yearly_breakdown: list[dict[str, float]] = field(default_factory=list)


@dataclass
class GSTResult:
    """Result of a GST calculation."""
    base_amount: float
    gst_rate: float
    cgst: float
    sgst: float
    igst: float
    total_gst: float
    total_amount: float
    is_interstate: bool


@dataclass
class BudgetResult:
    """Result of a budget plan calculation."""
    monthly_income: float
    needs: float       # 50%
    wants: float       # 30%
    savings: float     # 20%
    breakdown: dict[str, float] = field(default_factory=dict)


@dataclass
class FinancialHealthResult:
    """Result of a financial health assessment."""
    score: int                          # 0-100
    grade: str                          # A+ to F
    savings_ratio: float
    debt_to_income: float
    expense_ratio: float
    emergency_months: float
    category_scores: dict[str, int] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
#  EMI CALCULATOR
# ═══════════════════════════════════════════════════════════════

def calculate_emi(
    principal: float,
    annual_rate: float,
    tenure_years: int,
) -> EMIResult:
    """Calculate Equated Monthly Installment (EMI) for a loan.

    Uses the standard EMI formula:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)

    Args:
        principal: Loan amount in INR.
        annual_rate: Annual interest rate (e.g. 8.5 for 8.5%).
        tenure_years: Loan tenure in years.

    Returns:
        EMIResult with monthly EMI, total payment, interest, and yearly breakdown.
    """
    if principal <= 0 or annual_rate <= 0 or tenure_years <= 0:
        return EMIResult(principal, annual_rate, tenure_years, 0, 0, 0)

    monthly_rate = annual_rate / (12 * 100)
    n_months = tenure_years * 12

    # EMI formula
    if monthly_rate == 0:
        emi = principal / n_months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** n_months / (
            (1 + monthly_rate) ** n_months - 1
        )

    total_payment = emi * n_months
    total_interest = total_payment - principal

    # Yearly breakdown
    yearly_breakdown = []
    balance = principal
    for year in range(1, tenure_years + 1):
        year_principal = 0.0
        year_interest = 0.0
        for _ in range(12):
            interest_part = balance * monthly_rate
            principal_part = emi - interest_part
            balance -= principal_part
            year_principal += principal_part
            year_interest += interest_part
        yearly_breakdown.append({
            "year": year,
            "principal_paid": round(year_principal, 2),
            "interest_paid": round(year_interest, 2),
            "balance": round(max(balance, 0), 2),
        })

    return EMIResult(
        principal=principal,
        annual_rate=annual_rate,
        tenure_years=tenure_years,
        monthly_emi=round(emi, 2),
        total_payment=round(total_payment, 2),
        total_interest=round(total_interest, 2),
        yearly_breakdown=yearly_breakdown,
    )


# ═══════════════════════════════════════════════════════════════
#  SIP CALCULATOR
# ═══════════════════════════════════════════════════════════════

def calculate_sip(
    monthly_investment: float,
    annual_return_rate: float,
    tenure_years: int,
    step_up_percent: float = 0.0,
) -> SIPResult:
    """Calculate future value of a Systematic Investment Plan (SIP).

    Args:
        monthly_investment: Monthly SIP amount in INR.
        annual_return_rate: Expected annual return rate (e.g. 12.0 for 12%).
        tenure_years: Investment period in years.
        step_up_percent: Annual step-up percentage (0 for flat SIP).

    Returns:
        SIPResult with future value, total invested, wealth gained, and yearly breakdown.
    """
    if monthly_investment <= 0 or tenure_years <= 0:
        return SIPResult(monthly_investment, annual_return_rate, tenure_years, 0, 0, 0)

    monthly_rate = annual_return_rate / (12 * 100)
    total_invested = 0.0
    future_value = 0.0
    current_sip = monthly_investment
    yearly_breakdown = []

    for year in range(1, tenure_years + 1):
        year_invested = 0.0
        for _ in range(12):
            future_value = (future_value + current_sip) * (1 + monthly_rate)
            total_invested += current_sip
            year_invested += current_sip

        yearly_breakdown.append({
            "year": year,
            "monthly_sip": round(current_sip, 2),
            "year_invested": round(year_invested, 2),
            "total_invested": round(total_invested, 2),
            "corpus": round(future_value, 2),
        })

        # Step-up
        if step_up_percent > 0:
            current_sip *= (1 + step_up_percent / 100)

    wealth_gained = future_value - total_invested

    return SIPResult(
        monthly_investment=monthly_investment,
        annual_return_rate=annual_return_rate,
        tenure_years=tenure_years,
        total_invested=round(total_invested, 2),
        future_value=round(future_value, 2),
        wealth_gained=round(wealth_gained, 2),
        yearly_breakdown=yearly_breakdown,
    )


# ═══════════════════════════════════════════════════════════════
#  COMPOUND INTEREST CALCULATOR
# ═══════════════════════════════════════════════════════════════

COMPOUNDING_FREQUENCIES = {
    "Annual": 1,
    "Semi-Annual": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365,
}


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    tenure_years: int,
    compounding: str = "Annual",
) -> CompoundInterestResult:
    """Calculate compound interest with configurable frequency.

    Formula: A = P × (1 + r/n)^(n×t)

    Args:
        principal: Initial investment amount.
        annual_rate: Annual interest rate (e.g. 7.0 for 7%).
        tenure_years: Investment period in years.
        compounding: Frequency — 'Annual', 'Semi-Annual', 'Quarterly', 'Monthly', 'Daily'.

    Returns:
        CompoundInterestResult with final amount, interest earned, and yearly breakdown.
    """
    if principal <= 0 or tenure_years <= 0:
        return CompoundInterestResult(principal, annual_rate, tenure_years, compounding, principal, 0)

    n = COMPOUNDING_FREQUENCIES.get(compounding, 1)
    r = annual_rate / 100

    yearly_breakdown = []
    for year in range(1, tenure_years + 1):
        amount = principal * (1 + r / n) ** (n * year)
        yearly_breakdown.append({
            "year": year,
            "amount": round(amount, 2),
            "interest_earned": round(amount - principal, 2),
        })

    final_amount = principal * (1 + r / n) ** (n * tenure_years)
    total_interest = final_amount - principal

    return CompoundInterestResult(
        principal=principal,
        annual_rate=annual_rate,
        tenure_years=tenure_years,
        compounding_frequency=compounding,
        final_amount=round(final_amount, 2),
        total_interest=round(total_interest, 2),
        yearly_breakdown=yearly_breakdown,
    )


# ═══════════════════════════════════════════════════════════════
#  GST CALCULATOR
# ═══════════════════════════════════════════════════════════════

def calculate_gst(
    base_amount: float,
    gst_rate: float,
    is_interstate: bool = False,
) -> GSTResult:
    """Calculate GST (Goods and Services Tax) on an amount.

    For intra-state: GST is split into CGST and SGST (each = rate/2).
    For inter-state: GST is charged as IGST (full rate).

    Args:
        base_amount: Base price before GST.
        gst_rate: GST rate percentage (e.g. 18.0 for 18%).
        is_interstate: True for inter-state transaction (IGST), False for intra-state (CGST+SGST).

    Returns:
        GSTResult with breakdown of CGST, SGST, IGST, total GST, and total amount.
    """
    total_gst = base_amount * gst_rate / 100

    if is_interstate:
        cgst = 0.0
        sgst = 0.0
        igst = total_gst
    else:
        cgst = total_gst / 2
        sgst = total_gst / 2
        igst = 0.0

    return GSTResult(
        base_amount=round(base_amount, 2),
        gst_rate=gst_rate,
        cgst=round(cgst, 2),
        sgst=round(sgst, 2),
        igst=round(igst, 2),
        total_gst=round(total_gst, 2),
        total_amount=round(base_amount + total_gst, 2),
        is_interstate=is_interstate,
    )


# ═══════════════════════════════════════════════════════════════
#  BUDGET PLANNER (50-30-20 Rule)
# ═══════════════════════════════════════════════════════════════

def calculate_budget(monthly_income: float) -> BudgetResult:
    """Calculate a budget using the 50-30-20 rule.

    - 50% for Needs (rent, food, utilities, insurance, EMIs)
    - 30% for Wants (entertainment, dining, shopping, travel)
    - 20% for Savings & Investments (SIP, PPF, FD, emergency fund)

    Args:
        monthly_income: Gross monthly income in INR.

    Returns:
        BudgetResult with category allocations and detailed breakdown.
    """
    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20

    breakdown = {
        "🏠 Rent / Housing": round(monthly_income * 0.25, 2),
        "🍽️ Food & Groceries": round(monthly_income * 0.10, 2),
        "⚡ Utilities & Bills": round(monthly_income * 0.08, 2),
        "🚌 Transport": round(monthly_income * 0.07, 2),
        "🎬 Entertainment": round(monthly_income * 0.10, 2),
        "🛍️ Shopping & Personal": round(monthly_income * 0.10, 2),
        "✈️ Travel & Leisure": round(monthly_income * 0.10, 2),
        "📈 SIP / Mutual Funds": round(monthly_income * 0.08, 2),
        "🏦 PPF / FD / NPS": round(monthly_income * 0.07, 2),
        "🆘 Emergency Fund": round(monthly_income * 0.05, 2),
    }

    return BudgetResult(
        monthly_income=round(monthly_income, 2),
        needs=round(needs, 2),
        wants=round(wants, 2),
        savings=round(savings, 2),
        breakdown=breakdown,
    )


# ═══════════════════════════════════════════════════════════════
#  SAVINGS GOAL PLANNER
# ═══════════════════════════════════════════════════════════════

def calculate_savings_goal(
    target_amount: float,
    current_savings: float,
    annual_return_rate: float,
    tenure_years: int,
) -> dict:
    """Calculate required monthly savings to reach a goal.

    Args:
        target_amount: Target savings amount in INR.
        current_savings: Current savings already accumulated.
        annual_return_rate: Expected annual return rate (e.g. 10.0 for 10%).
        tenure_years: Time horizon in years.

    Returns:
        Dictionary with monthly savings needed and projection details.
    """
    if tenure_years <= 0 or target_amount <= current_savings:
        return {
            "monthly_savings_needed": 0,
            "target_amount": target_amount,
            "current_savings": current_savings,
            "gap": max(0, target_amount - current_savings),
            "tenure_years": tenure_years,
        }

    monthly_rate = annual_return_rate / (12 * 100)
    n_months = tenure_years * 12

    # Future value of current savings
    fv_current = current_savings * (1 + monthly_rate) ** n_months

    # Remaining amount to be accumulated via monthly savings
    remaining = target_amount - fv_current

    if remaining <= 0:
        return {
            "monthly_savings_needed": 0,
            "target_amount": target_amount,
            "current_savings": current_savings,
            "future_value_of_current": round(fv_current, 2),
            "gap": 0,
            "message": "Your current savings will exceed your target!",
        }

    # Monthly savings using future value of annuity formula
    if monthly_rate == 0:
        monthly_needed = remaining / n_months
    else:
        monthly_needed = remaining * monthly_rate / ((1 + monthly_rate) ** n_months - 1)

    return {
        "monthly_savings_needed": round(monthly_needed, 2),
        "target_amount": target_amount,
        "current_savings": current_savings,
        "future_value_of_current": round(fv_current, 2),
        "gap": round(remaining, 2),
        "tenure_years": tenure_years,
        "annual_return_rate": annual_return_rate,
    }


# ═══════════════════════════════════════════════════════════════
#  FINANCIAL HEALTH SCORE
# ═══════════════════════════════════════════════════════════════

def calculate_financial_health(
    monthly_income: float,
    monthly_savings: float,
    total_debt: float,
    monthly_expenses: float,
    emergency_fund: float,
) -> FinancialHealthResult:
    """Calculate a comprehensive financial health score (0-100).

    Scoring dimensions:
    - Savings Ratio (25 pts): monthly_savings / monthly_income
    - Debt-to-Income (25 pts): total_debt / (monthly_income × 12)
    - Expense Ratio (25 pts): monthly_expenses / monthly_income
    - Emergency Fund (25 pts): emergency_fund / monthly_expenses (in months)

    Args:
        monthly_income: Gross monthly income.
        monthly_savings: Monthly savings amount.
        total_debt: Total outstanding debt.
        monthly_expenses: Monthly expenses (excluding savings).
        emergency_fund: Total emergency fund amount.

    Returns:
        FinancialHealthResult with score, grade, ratios, and personalized suggestions.
    """
    if monthly_income <= 0:
        return FinancialHealthResult(
            score=0, grade="N/A", savings_ratio=0, debt_to_income=0,
            expense_ratio=0, emergency_months=0,
            suggestions=["Please provide a valid monthly income to calculate your financial health."],
        )

    # ── Calculate Ratios ─────────────────────────────────────
    savings_ratio = monthly_savings / monthly_income
    annual_income = monthly_income * 12
    debt_to_income = total_debt / annual_income if annual_income > 0 else 0
    expense_ratio = monthly_expenses / monthly_income
    emergency_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0

    # ── Score: Savings Ratio (0-25) ──────────────────────────
    if savings_ratio >= 0.30:
        savings_score = 25
    elif savings_ratio >= 0.20:
        savings_score = 20
    elif savings_ratio >= 0.10:
        savings_score = 15
    elif savings_ratio >= 0.05:
        savings_score = 10
    else:
        savings_score = 5

    # ── Score: Debt-to-Income (0-25) ─────────────────────────
    if debt_to_income <= 0.1:
        debt_score = 25
    elif debt_to_income <= 0.3:
        debt_score = 20
    elif debt_to_income <= 0.5:
        debt_score = 15
    elif debt_to_income <= 0.8:
        debt_score = 10
    else:
        debt_score = 5

    # ── Score: Expense Ratio (0-25) ──────────────────────────
    if expense_ratio <= 0.50:
        expense_score = 25
    elif expense_ratio <= 0.65:
        expense_score = 20
    elif expense_ratio <= 0.75:
        expense_score = 15
    elif expense_ratio <= 0.90:
        expense_score = 10
    else:
        expense_score = 5

    # ── Score: Emergency Fund (0-25) ─────────────────────────
    if emergency_months >= 6:
        emergency_score = 25
    elif emergency_months >= 3:
        emergency_score = 20
    elif emergency_months >= 1:
        emergency_score = 15
    elif emergency_months > 0:
        emergency_score = 10
    else:
        emergency_score = 5

    total_score = savings_score + debt_score + expense_score + emergency_score

    # ── Grade ────────────────────────────────────────────────
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B+"
    elif total_score >= 60:
        grade = "B"
    elif total_score >= 50:
        grade = "C"
    elif total_score >= 40:
        grade = "D"
    else:
        grade = "F"

    # ── Personalized Suggestions ─────────────────────────────
    suggestions = []

    if savings_ratio < 0.20:
        suggestions.append(
            f"💡 Your savings rate is {savings_ratio:.0%}. Aim for at least 20% of income. "
            f"Consider automating a monthly SIP of ₹{monthly_income * 0.20 - monthly_savings:,.0f} more."
        )

    if debt_to_income > 0.3:
        suggestions.append(
            f"⚠️ Your debt-to-income ratio is {debt_to_income:.0%} (ideally below 30%). "
            f"Focus on paying off high-interest debt first (credit cards > personal loans > home loan)."
        )

    if expense_ratio > 0.70:
        suggestions.append(
            f"📊 You're spending {expense_ratio:.0%} of your income. Try the 50-30-20 rule: "
            f"50% needs, 30% wants, 20% savings."
        )

    if emergency_months < 6:
        target_emergency = monthly_expenses * 6
        gap = target_emergency - emergency_fund
        suggestions.append(
            f"🆘 Your emergency fund covers {emergency_months:.1f} months. "
            f"Target 6 months (₹{target_emergency:,.0f}). You need ₹{gap:,.0f} more."
        )

    if not suggestions:
        suggestions.append(
            "🌟 Excellent financial health! Keep up the great work. "
            "Consider diversifying investments or increasing SIP contributions."
        )

    return FinancialHealthResult(
        score=total_score,
        grade=grade,
        savings_ratio=round(savings_ratio, 4),
        debt_to_income=round(debt_to_income, 4),
        expense_ratio=round(expense_ratio, 4),
        emergency_months=round(emergency_months, 1),
        category_scores={
            "Savings": savings_score,
            "Debt Management": debt_score,
            "Expense Control": expense_score,
            "Emergency Fund": emergency_score,
        },
        suggestions=suggestions,
    )
