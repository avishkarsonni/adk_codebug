import sys
import subprocess

AGENT_SCRIPTS = {
    'code_reader': 'code_reader_agent.py',
    'bug_identifier': 'bug_identifier_agent.py',
    'fix_recommender': 'fix_recommender_agent.py',
    'code_executor': 'code_executor_agent.py',
}

def run_agent(agent, file=None):
    script = AGENT_SCRIPTS.get(agent)
    if not script:
        print(f'Unknown agent: {agent}')
        return
    cmd = ['python', script]
    if file:
        cmd.append(file)
    print(f'Running: {" ".join(cmd)}')
    subprocess.run(cmd)

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py <agent> [file]')
        print('Agents:', ', '.join(AGENT_SCRIPTS.keys()))
        return
    agent = sys.argv[1]
    file = sys.argv[2] if len(sys.argv) > 2 else None
    run_agent(agent, file)

if __name__ == '__main__':
    main() 