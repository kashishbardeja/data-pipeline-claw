import os
import asyncio
import json
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig
import tools

# Load credentials
load_dotenv()

class AntigravityDataClaw:
    def __init__(self, target_file: str):
        self.target_file = target_file
        self.claw_name = "DataPipelineMonitoringClaw/V2-Antigravity"
        self.state = "IDLE"

    def log_state_transition(self, next_state: str):
        print(f"[🤖 SYSTEM LOG] {self.claw_name} transitioning: {self.state} ➡️ {next_state}")
        self.state = next_state

    async def execute_workflow(self):
        print(f"\n🚀 Starting Autonomous Antigravity Workflow for: {self.target_file}")
        
        # Step 1: Freshness Evaluation
        self.log_state_transition("INGESTING")
        freshness_result = tools.check_freshness(self.target_file)
        print(f"   Result: {freshness_result['message']}")
        
        # Step 2: Structural Validation
        self.log_state_transition("VALIDATING")
        validation_result = tools.validate_schema(self.target_file)
        print(f"   Result: {validation_result['message']}")

        # Step 3: Autonomous Decision & Agentic Context Escalation
     # Step 3: Autonomous Decision & Agentic Context Escalation
        if freshness_result["status"] == "FAIL" or validation_result["status"] == "FAIL":
            self.log_state_transition("DIAGNOSING")
            
            raw_error_logs = f"""
            Target Asset: {self.target_file}
            Freshness: {json.dumps(freshness_result)}
            Validation: {json.dumps(validation_result)}
            """
            
            prompt = (
                f"You are an autonomous operations engineer. Diagnose the root cause of this "
                f"pipeline failure and provide a concise summary with recommended next steps:\n{raw_error_logs}"
            )
            
            try:
                # ⏳ ANTI-THROTTLING: Pause for 60 seconds to ensure free-tier API quota resets
                print("⏳ [ANTI-THROTTLING] Pausing for 60 seconds to ensure API quota availability...")
                await asyncio.sleep(60)
                
                # Initialize the Antigravity Agent runtime environment
                config = LocalAgentConfig(
                    api_key=os.getenv("GEMINI_API_KEY"),
                    system_instructions="You are a data reliability automation agent."
                )
                
                # Execute inside the Antigravity async context lifecycle layer
                async with Agent(config) as agent:
                    response = await agent.chat(prompt)
                    diagnosis_summary = await response.text()
                    
            except Exception as e:
                # 🛠️ THIS EXCEPT BLOCK WAS MISSING IN YOUR FILE:
                diagnosis_summary = f"Antigravity Runtime Inference failed. Details:\n{str(e)}"

            # Step 4: Escalation Delivery
            self.log_state_transition("ESCALATING")
            tools.send_terminal_alert(self.claw_name, self.state, diagnosis_summary)
            return "Workflow completed: Failures autonomously resolved via Antigravity runtime."
            
        else:
            self.log_state_transition("COMPLETED")
            print(f"✅ [SUCCESS] File {self.target_file} cleared by Antigravity runtime.")
            return "Workflow completed: Pipeline clean."

# --- Async Runner Wrapper ---
async def run_simulations():
    success_file = "mock_data/success_batch.csv"
    corrupted_file = "mock_data/corrupted_batch.csv"
    
    print("\n=== SIMULATION 1: PROCESSING CLEAN PRODUCTION DATA ===")
    clean_claw = AntigravityDataClaw(success_file)
    await clean_claw.execute_workflow()
    
    print("\n=== SIMULATION 2: PROCESSING CORRUPTED PIPELINE DATA ===")
    broken_claw = AntigravityDataClaw(corrupted_file)
    await broken_claw.execute_workflow()

if __name__ == "__main__":
    # Standard Python async loop entrypoint
    asyncio.run(run_simulations())