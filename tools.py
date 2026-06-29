"""
ArthaMind AI — Tool Definitions Module
========================================
LangChain-compatible tool definitions for the AI agent.
Each tool encapsulates a financial calculation or API call.
"""

from typing import Optional

from langchain_core.tools import tool

from calculators import (
    calculate_compound_interest,
    calculate_emi,
    calculate_gst,
    calculate_sip,
    calculate_budget,
    calculate_savings_goal,
    calculate_financial_health,
)
from market import CurrencyConverter, MetalPriceFetcher
from utils import format_currency, logger


# ═══════════════════════════════════════════════════════════════
#  MARKET DATA TOOLS
# ═══════════════════════════════════════════════════════════════

@tool
def get_gold_price() -> str:
    """Get the current gold price in Indian Rupees (INR) per gram and per 10 grams for 24K and 22K purity.

    Returns:
        Formatted gold price information.
    """
    try:
        data = MetalPriceFetcher.get_gold_price()
        if data.get("status") == "live":
            return (
                f"🥇 **Live Gold Prices in India**\n\n"
                f"| Purity | Per Gram | Per 10 Grams |\n"
                f"|--------|----------|-------------|\n"
                f"| 24K (999) | {format_currency(data['price_per_gram_24k'])} | {format_currency(data['price_per_10g_24k'])} |\n"
                f"| 22K (916) | {format_currency(data['price_per_gram_22k'])} | {format_currency(data['price_per_10g_22k'])} |\n\n"
                f"📡 Source: {data['source']} | 🕐 {data['timestamp']}"
            )
        return f"Gold prices are currently unavailable. {data.get('source', '')}"
    except Exception as exc:
        logger.error(f"Gold price tool error: {exc}")
        return "Unable to fetch gold prices at the moment. Please try again later."


@tool
def get_silver_price() -> str:
    """Get the current silver price in Indian Rupees (INR) per gram and per kilogram.

    Returns:
        Formatted silver price information.
    """
    try:
        data = MetalPriceFetcher.get_silver_price()
        if data.get("status") == "live":
            return (
                f"🥈 **Live Silver Prices in India**\n\n"
                f"| Unit | Price |\n"
                f"|------|-------|\n"
                f"| Per Gram | {format_currency(data['price_per_gram'])} |\n"
                f"| Per Kilogram | {format_currency(data['price_per_kg'])} |\n\n"
                f"📡 Source: {data['source']} | 🕐 {data['timestamp']}"
            )
        return f"Silver prices are currently unavailable. {data.get('source', '')}"
    except Exception as exc:
        logger.error(f"Silver price tool error: {exc}")
        return "Unable to fetch silver prices at the moment. Please try again later."


# ═══════════════════════════════════════════════════════════════
#  GST TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def gst_calculator(base_amount: float, gst_rate: float, is_interstate: bool = False) -> str:
    """Calculate GST (Goods and Services Tax) on a given amount.

    Args:
        base_amount: Base price of goods/services before GST in INR.
        gst_rate: GST rate percentage (e.g. 5, 12, 18, or 28).
        is_interstate: True for inter-state (IGST), False for intra-state (CGST+SGST).

    Returns:
        Formatted GST calculation breakdown.
    """
    result = calculate_gst(base_amount, gst_rate, is_interstate)
    transaction_type = "Inter-State (IGST)" if is_interstate else "Intra-State (CGST + SGST)"

    output = (
        f"🧮 **GST Calculation**\n\n"
        f"| Item | Amount |\n"
        f"|------|--------|\n"
        f"| Base Amount | {format_currency(result.base_amount)} |\n"
        f"| GST Rate | {result.gst_rate}% |\n"
        f"| Transaction | {transaction_type} |\n"
    )

    if is_interstate:
        output += f"| IGST | {format_currency(result.igst)} |\n"
    else:
        output += (
            f"| CGST ({result.gst_rate/2}%) | {format_currency(result.cgst)} |\n"
            f"| SGST ({result.gst_rate/2}%) | {format_currency(result.sgst)} |\n"
        )

    output += (
        f"| **Total GST** | **{format_currency(result.total_gst)}** |\n"
        f"| **Total Amount** | **{format_currency(result.total_amount)}** |\n"
    )
    return output


# ═══════════════════════════════════════════════════════════════
#  EMI TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def emi_calculator(principal: float, annual_rate: float, tenure_years: int) -> str:
    """Calculate EMI (Equated Monthly Installment) for a loan.

    Args:
        principal: Loan amount in INR.
        annual_rate: Annual interest rate in percentage (e.g. 8.5 for 8.5%).
        tenure_years: Loan tenure in years.

    Returns:
        Formatted EMI calculation with breakdown.
    """
    result = calculate_emi(principal, annual_rate, tenure_years)

    output = (
        f"🏦 **EMI Calculation**\n\n"
        f"| Parameter | Value |\n"
        f"|-----------|-------|\n"
        f"| Loan Amount | {format_currency(result.principal)} |\n"
        f"| Interest Rate | {result.annual_rate}% p.a. |\n"
        f"| Tenure | {result.tenure_years} years ({result.tenure_years * 12} months) |\n"
        f"| **Monthly EMI** | **{format_currency(result.monthly_emi)}** |\n"
        f"| Total Payment | {format_currency(result.total_payment)} |\n"
        f"| Total Interest | {format_currency(result.total_interest)} |\n"
    )
    return output


# ═══════════════════════════════════════════════════════════════
#  SIP TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def sip_calculator(monthly_investment: float, annual_return_rate: float, tenure_years: int) -> str:
    """Calculate future value of a SIP (Systematic Investment Plan) in mutual funds.

    Args:
        monthly_investment: Monthly SIP amount in INR.
        annual_return_rate: Expected annual return rate in percentage (e.g. 12.0).
        tenure_years: Investment period in years.

    Returns:
        Formatted SIP projection with total invested, corpus, and wealth gained.
    """
    result = calculate_sip(monthly_investment, annual_return_rate, tenure_years)

    output = (
        f"📈 **SIP Calculator**\n\n"
        f"| Parameter | Value |\n"
        f"|-----------|-------|\n"
        f"| Monthly SIP | {format_currency(result.monthly_investment)} |\n"
        f"| Expected Return | {result.annual_return_rate}% p.a. |\n"
        f"| Duration | {result.tenure_years} years |\n"
        f"| Total Invested | {format_currency(result.total_invested)} |\n"
        f"| **Expected Corpus** | **{format_currency(result.future_value)}** |\n"
        f"| Wealth Gained | {format_currency(result.wealth_gained)} |\n"
    )
    return output


# ═══════════════════════════════════════════════════════════════
#  COMPOUND INTEREST TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def compound_interest_calculator(
    principal: float, annual_rate: float, tenure_years: int, compounding: str = "Annual"
) -> str:
    """Calculate compound interest on an investment or deposit.

    Args:
        principal: Initial investment amount in INR.
        annual_rate: Annual interest rate in percentage (e.g. 7.0).
        tenure_years: Investment period in years.
        compounding: Compounding frequency — Annual, Semi-Annual, Quarterly, Monthly, or Daily.

    Returns:
        Formatted compound interest result.
    """
    result = calculate_compound_interest(principal, annual_rate, tenure_years, compounding)

    output = (
        f"💰 **Compound Interest Calculator**\n\n"
        f"| Parameter | Value |\n"
        f"|-----------|-------|\n"
        f"| Principal | {format_currency(result.principal)} |\n"
        f"| Interest Rate | {result.annual_rate}% p.a. |\n"
        f"| Tenure | {result.tenure_years} years |\n"
        f"| Compounding | {result.compounding_frequency} |\n"
        f"| **Maturity Amount** | **{format_currency(result.final_amount)}** |\n"
        f"| Interest Earned | {format_currency(result.total_interest)} |\n"
    )
    return output


# ═══════════════════════════════════════════════════════════════
#  CURRENCY CONVERTER TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def currency_converter(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another using live exchange rates.

    Args:
        amount: Amount to convert.
        from_currency: Source currency code (e.g. 'INR', 'USD').
        to_currency: Target currency code (e.g. 'USD', 'EUR').

    Returns:
        Formatted conversion result with exchange rate.
    """
    result = CurrencyConverter.convert(amount, from_currency, to_currency)

    if result.get("status") == "success":
        return (
            f"💱 **Currency Conversion**\n\n"
            f"| | |\n|---|---|\n"
            f"| Amount | {amount:,.2f} {from_currency} |\n"
            f"| Converted | **{result['converted_amount']:,.2f} {to_currency}** |\n"
            f"| Exchange Rate | 1 {from_currency} = {result['rate']:.6f} {to_currency} |\n"
            f"| Date | {result['date']} |\n"
        )
    return f"Currency conversion failed: {result.get('error', 'Unknown error')}"


# ═══════════════════════════════════════════════════════════════
#  BUDGET PLANNER TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def budget_planner(monthly_income: float) -> str:
    """Create a budget plan using the 50-30-20 rule for a given monthly income.

    Args:
        monthly_income: Monthly income in INR.

    Returns:
        Formatted budget plan with category allocations.
    """
    result = calculate_budget(monthly_income)

    output = (
        f"📋 **Budget Plan (50-30-20 Rule)**\n\n"
        f"**Monthly Income:** {format_currency(result.monthly_income)}\n\n"
        f"| Category | Allocation | Amount |\n"
        f"|----------|------------|--------|\n"
        f"| 🔵 Needs (50%) | Essential expenses | {format_currency(result.needs)} |\n"
        f"| 🟡 Wants (30%) | Lifestyle & leisure | {format_currency(result.wants)} |\n"
        f"| 🟢 Savings (20%) | Investments & goals | {format_currency(result.savings)} |\n\n"
        f"**Detailed Breakdown:**\n\n"
        f"| Category | Amount |\n"
        f"|----------|--------|\n"
    )
    for category, amount in result.breakdown.items():
        output += f"| {category} | {format_currency(amount)} |\n"

    return output


# ═══════════════════════════════════════════════════════════════
#  FINANCIAL HEALTH TOOL
# ═══════════════════════════════════════════════════════════════

@tool
def financial_health_check(
    monthly_income: float,
    monthly_savings: float,
    total_debt: float,
    monthly_expenses: float,
    emergency_fund: float,
) -> str:
    """Analyze financial health based on income, savings, debt, expenses, and emergency fund.

    Args:
        monthly_income: Gross monthly income in INR.
        monthly_savings: Monthly savings amount in INR.
        total_debt: Total outstanding debt in INR.
        monthly_expenses: Monthly expenses in INR.
        emergency_fund: Total emergency fund amount in INR.

    Returns:
        Financial health score, grade, and personalized suggestions.
    """
    result = calculate_financial_health(
        monthly_income, monthly_savings, total_debt, monthly_expenses, emergency_fund
    )

    output = (
        f"📊 **Financial Health Report**\n\n"
        f"## Score: {result.score}/100 — Grade: {result.grade}\n\n"
        f"| Dimension | Score | Status |\n"
        f"|-----------|-------|--------|\n"
    )

    for dimension, score in result.category_scores.items():
        status = "🟢 Excellent" if score >= 22 else "🟡 Good" if score >= 17 else "🟠 Fair" if score >= 12 else "🔴 Needs Work"
        output += f"| {dimension} | {score}/25 | {status} |\n"

    output += "\n**Key Ratios:**\n\n"
    output += (
        f"| Ratio | Value | Ideal |\n"
        f"|-------|-------|-------|\n"
        f"| Savings Rate | {result.savings_ratio:.0%} | ≥ 20% |\n"
        f"| Debt-to-Income | {result.debt_to_income:.0%} | ≤ 30% |\n"
        f"| Expense Ratio | {result.expense_ratio:.0%} | ≤ 70% |\n"
        f"| Emergency Fund | {result.emergency_months:.1f} months | ≥ 6 months |\n"
    )

    output += "\n**💡 Suggestions:**\n\n"
    for suggestion in result.suggestions:
        output += f"- {suggestion}\n"

    return output


# ═══════════════════════════════════════════════════════════════
#  TOOL REGISTRY
# ═══════════════════════════════════════════════════════════════

ALL_TOOLS = [
    get_gold_price,
    get_silver_price,
    gst_calculator,
    emi_calculator,
    sip_calculator,
    compound_interest_calculator,
    currency_converter,
    budget_planner,
    financial_health_check,
]
