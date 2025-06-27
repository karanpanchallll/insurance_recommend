def build_prompt_with_search(user_profile, search_results):
    # Format the top 10 results to allow Gemini to pick the best 7
    result_text = "\n".join([
        f"{i+1}. {r['title']}\n{r['snippet']}\nLink: {r['link']}\n" 
        for i, r in enumerate(search_results[:10])
    ])

    income = user_profile["Income Level"]
    affordability_note = ""

    if income < 100000:
        affordability_note = "⚠️ The user has a very low income. Please recommend only affordable policies with low premiums and basic coverage."
    elif income < 350000:
        affordability_note = "⚠️ Moderate income. Keep premiums under ₹1000/month and coverage under ₹5 lakh if possible."

    prompt = f'''
You are an experienced and responsible insurance advisor.

Your task is to:
1. Analyze the user profile and risk factors.
2. Filter and recommend the **top 7 most suitable insurance policies** from the search results.
3. Justify each recommendation clearly.

User Profile:
{user_profile}

{affordability_note}

Search Results:
{result_text}

Respond strictly in this format:

### 🛡️ Underwriting Decision:
- **Risk Category**: Low / Medium / High
- **Eligible for**: <List of suitable insurance types>
- **Exclusions (if any)**: ...
- **Suggested Coverage**: ...
- **Suggested Premium**: ...

### 🏆 Top 7 Recommended Policies:

1. **<Policy Name 1>**  
   🔗 [Link](<URL>)  
   💸 **Premium**: <₹ amount / N/A>  
   💼 **Coverage**: <Coverage details or N/A>  
   📊 **Claim Ratio**: <Ratio or N/A>  
   📝 **Reason**: <Explain why this policy fits the user based on risk, income, preference, etc.>

2. **<Policy Name 2>**  
   🔗 [Link](<URL>)  
   💸 **Premium**: ...  
   💼 **Coverage**: ...  
   📊 **Claim Ratio**: ...  
   📝 **Reason**: ...

...and so on till 7.
'''
    return prompt
