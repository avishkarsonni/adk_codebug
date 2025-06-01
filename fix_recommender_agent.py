import json
import re

BUG_REPORT_FILE = 'bug_report.json'
FIX_SUGGESTIONS_FILE = 'fix_suggestions.json'

# Simple fix recommender for demonstration

def suggest_fix(error):
    msg = error.get('msg', '').lower()
    if 'missing colon' in msg or 'expected' in msg and ':' in msg:
        return 'Add a colon at the indicated line.'
    if 'unexpected indent' in msg:
        return 'Check indentation at the indicated line.'
    if 'syntaxerror' in error.get('type', '').lower():
        return 'Check Python syntax at the indicated line.'
    return 'Review the error message and correct the code.'

def recommend_fixes():
    with open(BUG_REPORT_FILE, 'r') as f:
        bug_report = json.load(f)
    suggestions = []
    for file_report in bug_report:
        file_suggestions = []
        for error in file_report.get('errors', []):
            file_suggestions.append({
                'line': error.get('line'),
                'error': error.get('msg'),
                'suggestion': suggest_fix(error)
            })
        suggestions.append({
            'file': file_report['file'],
            'fixes': file_suggestions
        })
    with open(FIX_SUGGESTIONS_FILE, 'w') as f:
        json.dump(suggestions, f, indent=2)
    return suggestions

if __name__ == '__main__':
    result = recommend_fixes()
    print(json.dumps(result, indent=2)) 