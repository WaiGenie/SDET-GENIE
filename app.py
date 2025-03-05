import streamlit as st
import sys
import asyncio
import os
import re
from dotenv import load_dotenv

from src.Agents.agents import qa_agent

from browser_use import Browser, Agent as BrowserAgent
from src.Utilities.utils import controller
from langchain_google_genai import ChatGoogleGenerativeAI

from src.Prompts.agno_prompts import (
    generate_selenium_pytest_bdd,
    generate_playwright_python,
    generate_cypress_js,
    generate_robot_framework,
    generate_java_selenium,
    generate_gherkin_scenarios,
)

from src.Prompts.browser_prompts import generate_browser_task

# Load environment variables
load_dotenv()

# Handle Windows asyncio policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# Dictionary mapping framework names to their generation functions
FRAMEWORK_GENERATORS = {
    "Selenium + PyTest BDD (Python)": generate_selenium_pytest_bdd,
    "Playwright (Python)": generate_playwright_python,
    "Cypress (JavaScript)": generate_cypress_js,
    "Robot Framework": generate_robot_framework,
    "Selenium + Cucumber (Java)": generate_java_selenium,
}

# Dictionary mapping framework names to their file extensions
FRAMEWORK_EXTENSIONS = {
    "Selenium + PyTest BDD (Python)": "py",
    "Playwright (Python)": "py",
    "Cypress (JavaScript)": "js",
    "Robot Framework": "robot",
    "Selenium + Cucumber (Java)": "java",
}

# Framework descriptions
framework_descriptions = {
    "Selenium + PyTest BDD (Python)": "Popular Python testing framework combining Selenium WebDriver with PyTest BDD for behavior-driven development. Best for Python developers who want strong test organization and reporting.",
    "Playwright (Python)": "Modern, powerful browser automation framework with built-in async support and cross-browser testing capabilities. Excellent for modern web applications and complex scenarios.",
    "Cypress (JavaScript)": "Modern, JavaScript-based end-to-end testing framework with real-time reloading and automatic waiting. Perfect for front-end developers and modern web applications.",
    "Robot Framework": "Keyword-driven testing framework that uses simple, tabular syntax. Great for teams with mixed technical expertise and for creating readable test cases.",
    "Selenium + Cucumber (Java)": "Robust combination of Selenium WebDriver with Cucumber for Java, supporting BDD. Ideal for Java teams and enterprise applications.",
}


def main():

    st.set_page_config(page_title="SDET-GENIE", layout="wide")

    # Apply custom CSS
    st.markdown(
        """
    <style>
        .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: auto;
            max-width: 600px;
        }
        .stButton > button {
            width: 100%;
            padding: 0;
        }
        .button-container > div {
            text-align: center;
        }
        .text-area-container {
            width: 600px;
            margin: 0 auto;
        }
        .stTextArea textarea {
            width: 100% !important;
            height: 150px !important;
            font-size: 16px !important;
            border: 1px solid #ccc !important;
            padding: 10px !important;
        }
        /*
        .stMain {
            background: linear-gradient(135deg, #FFFFFF, rgba(81, 162, 255, 0.5))
        }
        */
        .block-container {
            width: 700px;
            padding-top: 20px;
        }
        .stMarkdown > div > p {
            margin: 0;
            font-size: 16px;
        }
        .stTextArea label div p {
            font-weight: bold;
        }
        .user-story {
            margin: 0;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown('<section class="all-container">', unsafe_allow_html=True)

    # Custom Header
    st.markdown(
        '<div class="header fade-in" style="padding-top: 20px;"><span class="header-item">AI Agents powered by AGNO and BROWSER-USE</span></div>',
        unsafe_allow_html=True,
    )

    # Main Title with custom styling
    st.markdown(
        '<h1 class="main-title fade-in">SDET - GENIE</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle fade-in">User Stories to Automated Tests : The Future of QA Automation using AI Agents</p>',
        unsafe_allow_html=True,
    )
    # Sidebar styling
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-heading"><a href="https://www.waigenie.tech/" target="_blank" style="color: white; text-decoration: none;">WAIGENIE</a></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-heading">Avilable Frameworks</div>',
            unsafe_allow_html=True,
        )
        selected_framework = st.selectbox(
            "Select framework:", list(FRAMEWORK_GENERATORS.keys()), index=0
        )
        # New About WaiGenie section with tabs
        with st.expander("About WaiGenie"):
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["Vision & Mission", "Features", "How It Works", "Workflow", "Benefits"]
            )

            with tab1:
                st.subheader("Our Vision")
                st.write(
                    "Revolutionizing Quality Assurance with AI-powered solutions that empower teams to deliver flawless software at unprecedented speeds."
                )

                st.subheader("Our Mission")
                st.write(
                    "Empower QA teams with cutting-edge AI solutions tailored for enterprise needs, enabling them to deliver high-quality software faster and more efficiently than ever before."
                )

            with tab2:
                st.markdown("#### 🧠 AI-Powered Test Generation")
                st.write(
                    "Generate comprehensive test scenarios using advanced AI algorithms."
                )
                st.markdown("#### 🔍 Intelligent Element Inspector")
                st.write(
                    "Automatically identify and analyze web elements with precision."
                )
                st.markdown("#### 📝 Gherkin Feature Generator")
                st.write(
                    "Transform user stories into clear, concise Gherkin feature files."
                )
                st.markdown("#### 💻 Automated Code Generation")
                st.write(
                    "Generate test automation scripts in multiple languages automatically."
                )
                st.markdown("#### 🤖 Web Agent Explorer")
                st.write(
                    "Leverage AI to automatically explore and test complex user journeys."
                )
                st.markdown("#### 📊 Advanced Analytics")
                st.write(
                    "Gain insights into your testing processes and identify areas for improvement."
                )

            with tab3:
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown("### 1")
                with col2:
                    st.markdown("#### Sign Up")
                    st.write(
                        "Create your WaiGenie account and set up your organization profile."
                    )
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown("### 2")
                with col2:
                    st.markdown("#### Connect")
                    st.write(
                        "Integrate WaiGenie with your existing QA tools and workflows."
                    )
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown("### 3")
                with col2:
                    st.markdown("#### Analyze")
                    st.write(
                        "Let our AI analyze your application and generate test scenarios."
                    )
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown("### 4")
                with col2:
                    st.markdown("#### Optimize")
                    st.write(
                        "Continuously improve your QA process with AI-driven insights."
                    )

            with tab4:
                st.subheader("AI-Powered QA Workflow")
                st.markdown("#### 1. QA Agent")
                st.write("• Converts user stories into Gherkin scenarios")
                st.write("• Generates positive and negative test cases")
                st.markdown("#### 2. Browser Agent")
                st.write("• Executes Gherkin scenarios in a browser")
                st.write("• Captures detailed DOM information")
                st.write("• Records element details like XPaths")
                st.markdown("#### 3. Code Generation Agent")
                st.write("• Transforms scenarios into automation scripts")
                st.write("• Includes necessary imports and dependencies")
                st.write("• Handles errors and provides helper functions")

            with tab5:
                st.write("• 90% reduction in time-to-test")
                st.write("• Enhanced test coverage")
                st.write("• Consistent code implementation")
                st.write("• Lower maintenance overhead")
                st.write("• Bridges skill gaps")
                st.write("• Preserves testing knowledge")
            # Add contact button and separator
            st.markdown("---")
            email = "richardsongunde@waigenie.tech"
            gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}"
            st.markdown(
                f'<a href="{gmail_link}" target="_blank"><button style="width: 100%; background: rgba(81, 162, 255); color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">Contact Us</button></a>',
                unsafe_allow_html=True,
            )
            # Add logo and branding at the bottom
            st.markdown(
                """
            <div style="text-align: center; margin-top: 30px;">
                <img src="https://www.waigenie.tech/logo.png" style="width: 96px; height: auto; margin-bottom: 10px;">
                <img src="https://www.waigenie.tech/logotext.svg" style="width: 180px; height: auto; display: block; margin: 0 auto;">
                <p style="font-size: 0.75rem; color: #E6E6FA; margin-top: 10px;">© 2025 www.waigenie.tech. All rights reserved.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Add YouTube demo button
        youtube_url = "https://youtu.be/qH30GvQebqg?feature=shared"
        st.markdown(
            f'<a href="{youtube_url}" target="_blank"><button style="width: 100%; background: rgb(255, 44, 54); color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">▶️  YouTube Demo</button></a>',
            unsafe_allow_html=True,
        )

    # Main content area with card styling
    st.markdown('<div class="text-area-container">', unsafe_allow_html=True)
    # st.markdown('<span style="margin: 0;">Enter User Story</span>', unsafe_allow_html=True)
    user_story = st.text_area(
        "Enter User Story",
        placeholder="e.g., As a user, I want to log in with valid credentials so that I can access my account.",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    # Ask user to choose a button
    st.markdown('<span style="margin: 0; font-weight: bold;">Choose your desired action: </span>', unsafe_allow_html=True)
    st.markdown('<span style="margin: 0; font-size: 14px; font-weight: light;">You can choose your desired framework from the sidebar...</span>', unsafe_allow_html=True)
    # Buttons with better layout
    col0, col1, col2 = st.columns(3)
    with col0:
        st.markdown("<div>", unsafe_allow_html=True)
        generate_btn = st.button("🔍 Generate Gherkin")
        st.markdown("</div>", unsafe_allow_html=True)
    with col1:
        st.markdown("<div>", unsafe_allow_html=True)
        execute_btn = st.button("▶️ Execute Steps")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div>", unsafe_allow_html=True)
        generate_code_btn = st.button("💻 Generate Code")
        st.markdown("</div>", unsafe_allow_html=True)
    # Gherkin Generation Section
    if generate_btn and user_story:
        with st.spinner("Generating Gherkin scenarios..."):
            prompt = generate_gherkin_scenarios(user_story)
            run_response = qa_agent.run(prompt)
            generated_steps = run_response.content
            st.session_state.generated_steps = generated_steps

            st.markdown(
                '<div class="card code-container fade-in">', unsafe_allow_html=True
            )
            st.markdown(
                '<h3 class="glow-text">Generated Gherkin Scenarios</h3>',
                unsafe_allow_html=True,
            )
            st.code(generated_steps, language="gherkin")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                '<div class="status-success fade-in">Gherkin scenarios generated successfully!</div>',
                unsafe_allow_html=True,
            )
    # Test Execution Section
    if execute_btn:
        if "generated_steps" not in st.session_state:
            st.markdown(
                '<div class="status-error">Please generate Gherkin scenarios first.</div>',
                unsafe_allow_html=True,
            )
        else:
            # Modify the execute_test function to store more detailed information
            async def execute_test(steps: str):
                try:
                    browser = Browser()

                    async with await browser.new_context() as context:
                        # Parse the Gherkin content to extract scenarios
                        scenarios = []
                        current_scenario = []
                        for line in steps.split("\n"):
                            if line.strip().startswith("Scenario:"):
                                if current_scenario:
                                    scenarios.append("\n".join(current_scenario))
                                current_scenario = [line]
                            elif current_scenario:
                                current_scenario.append(line)
                        if current_scenario:
                            scenarios.append("\n".join(current_scenario))

                        # Execute each scenario separately
                        all_results = []
                        all_actions = []
                        all_extracted_content = []
                        element_xpath_map = {}

                        for scenario in scenarios:
                            browser_agent = BrowserAgent(
                                task=generate_browser_task(scenario),
                                llm=ChatGoogleGenerativeAI(
                                    model="gemini-2.0-flash",
                                    api_key=os.environ.get("GOOGLE_API_KEY"),
                                ),
                                browser=browser,
                                controller=controller,
                            )

                            # Execute and collect results
                            history = await browser_agent.run()
                            history.save_to_file("agent_history.json")
                            result = history.final_result()
                            if isinstance(result, str):
                                # Convert string result to JSON format
                                result = {
                                    "status": result,
                                    "details": "Execution completed",
                                }
                            all_results.append(result)

                            # Log all model actions for debugging
                            st.write("Debug - Model Actions:", history.model_actions())

                            # Process model actions to extract element details
                            for i, action_data in enumerate(history.model_actions()):
                                action_name = (
                                    history.action_names()[i]
                                    if i < len(history.action_names())
                                    else "Unknown Action"
                                )

                                # Create a detail record for each action
                                action_detail = {
                                    "name": action_name,
                                    "index": i,
                                    "element_details": {},
                                }

                                # Check if this is a get_xpath_of_element action
                                if "get_xpath_of_element" in action_data:
                                    element_index = action_data[
                                        "get_xpath_of_element"
                                    ].get("index")
                                    action_detail["element_details"][
                                        "index"
                                    ] = element_index

                                    # Check if the interacted_element field contains XPath information
                                    if (
                                        "interacted_element" in action_data
                                        and action_data["interacted_element"]
                                    ):
                                        element_info = action_data["interacted_element"]

                                        # Extract XPath from the DOMHistoryElement string
                                        xpath_match = re.search(
                                            r"xpath='([^']+)'", str(element_info)
                                        )
                                        if xpath_match:
                                            xpath = xpath_match.group(1)
                                            element_xpath_map[element_index] = xpath
                                            action_detail["element_details"][
                                                "xpath"
                                            ] = xpath

                                # Check if this is an action on an element
                                elif any(
                                    key in action_data
                                    for key in [
                                        "input_text",
                                        "click_element",
                                        "perform_element_action",
                                    ]
                                ):
                                    # Find the action parameters
                                    for key in [
                                        "input_text",
                                        "click_element",
                                        "perform_element_action",
                                    ]:
                                        if key in action_data:
                                            action_params = action_data[key]
                                            if "index" in action_params:
                                                element_index = action_params["index"]
                                                action_detail["element_details"][
                                                    "index"
                                                ] = element_index

                                                # If we have already captured the XPath for this element, add it
                                                if element_index in element_xpath_map:
                                                    action_detail["element_details"][
                                                        "xpath"
                                                    ] = element_xpath_map[element_index]

                                                # Also check interacted_element
                                                if (
                                                    "interacted_element" in action_data
                                                    and action_data[
                                                        "interacted_element"
                                                    ]
                                                ):
                                                    element_info = action_data[
                                                        "interacted_element"
                                                    ]
                                                    xpath_match = re.search(
                                                        r"xpath='([^']+)'",
                                                        str(element_info),
                                                    )
                                                    if xpath_match:
                                                        xpath = xpath_match.group(1)
                                                        element_xpath_map[
                                                            element_index
                                                        ] = xpath
                                                        action_detail[
                                                            "element_details"
                                                        ]["xpath"] = xpath

                                all_actions.append(action_detail)

                            # Also extract from content if available
                            for content in history.extracted_content():
                                all_extracted_content.append(content)

                                # Look for XPath information in extracted content
                                if isinstance(content, str):
                                    xpath_match = re.search(
                                        r"The xpath of the element is (.+)", content
                                    )
                                    if xpath_match:
                                        xpath = xpath_match.group(1)
                                        # Try to match with an element index from previous actions
                                        index_match = re.search(
                                            r"element (\d+)", content
                                        )
                                        if index_match:
                                            element_index = int(index_match.group(1))
                                            element_xpath_map[element_index] = xpath

                        # Save combined history to session state
                        st.session_state.history = {
                            "urls": history.urls(),
                            "action_names": history.action_names(),
                            "detailed_actions": all_actions,
                            "element_xpaths": element_xpath_map,
                            "extracted_content": all_extracted_content,
                            "errors": history.errors(),
                            "model_actions": history.model_actions(),
                            "execution_date": st.session_state.get(
                                "execution_date", "Unknown"
                            ),
                        }

                        # Display test execution details
                        st.markdown(
                            '<div class="status-success fade-in">Test execution completed!</div>',
                            unsafe_allow_html=True,
                        )

                        # Display key information in tabs
                        st.markdown(
                            '<div class="tab-container fade-in">',
                            unsafe_allow_html=True,
                        )
                        tab1, tab2, tab3, tab4 = st.tabs(
                            ["Results", "Actions", "Elements", "Details"]
                        )
                        with tab1:
                            for i, result in enumerate(all_results):
                                st.markdown(
                                    f'<h4 class="glow-text">Scenario {i+1}</h4>',
                                    unsafe_allow_html=True,
                                )
                                st.json(result)

                        with tab2:
                            st.markdown(
                                '<h4 class="glow-text">Actions Performed</h4>',
                                unsafe_allow_html=True,
                            )
                            for i, action in enumerate(all_actions):
                                action_text = f"{i+1}. {action['name']}"
                                if (
                                    "element_details" in action
                                    and action["element_details"]
                                ):
                                    if "xpath" in action["element_details"]:
                                        action_text += f" (XPath: {action['element_details']['xpath']})"
                                    elif "index" in action["element_details"]:
                                        action_text += f" (Element index: {action['element_details']['index']})"
                                st.write(action_text)

                        with tab3:
                            st.markdown(
                                '<h4 class="glow-text">Element Details</h4>',
                                unsafe_allow_html=True,
                            )
                            if element_xpath_map:
                                # Create a dataframe for better visualization
                                import pandas as pd

                                element_df = pd.DataFrame(
                                    [
                                        {"Element Index": index, "XPath": xpath}
                                        for index, xpath in element_xpath_map.items()
                                    ]
                                )
                                st.dataframe(element_df)
                            else:
                                st.info(
                                    "No element XPaths were captured during test execution."
                                )

                                # Display raw DOM information for debugging
                                st.markdown(
                                    '<h4 class="glow-text">Raw DOM Information</h4>',
                                    unsafe_allow_html=True,
                                )
                                for i, action_data in enumerate(
                                    history.model_actions()
                                ):
                                    if (
                                        "interacted_element" in action_data
                                        and action_data["interacted_element"]
                                    ):
                                        st.write(
                                            f"Action {i}: {history.action_names()[i] if i < len(history.action_names()) else 'Unknown'}"
                                        )
                                        st.code(str(action_data["interacted_element"]))

                        with tab4:
                            st.markdown(
                                '<h4 class="glow-text">Extracted Content</h4>',
                                unsafe_allow_html=True,
                            )
                            for content in all_extracted_content:
                                st.write(content)
                        st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(
                        f'<div class="status-error">An error occurred during test execution: {str(e)}</div>',
                        unsafe_allow_html=True,
                    )

            st.session_state.execution_date = "February 26, 2025"
            asyncio.run(execute_test(st.session_state.generated_steps))
    # Code Generation Section
    if generate_code_btn:
        if (
            "generated_steps" not in st.session_state
            or "history" not in st.session_state
        ):
            st.markdown(
                '<div class="status-error">Please generate and execute Gherkin scenarios first.</div>',
                unsafe_allow_html=True,
            )
        else:
            with st.spinner(f"Generating {selected_framework} automation code..."):
                try:
                    # Get the appropriate generator function
                    generator_function = FRAMEWORK_GENERATORS[selected_framework]

                    # Generate automation code
                    automation_code = generator_function(
                        st.session_state.generated_steps, st.session_state.history
                    )

                    # Store in session state
                    st.session_state.automation_code = automation_code

                    # Display code
                    st.markdown(
                        '<div class="card code-container fade-in">',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<h3 class="glow-text">Generated {selected_framework} Automation Code</h3>',
                        unsafe_allow_html=True,
                    )

                    # Use appropriate language for syntax highlighting
                    code_language = "python"
                    if selected_framework == "Cypress (JavaScript)":
                        code_language = "javascript"
                    elif selected_framework == "Robot Framework":
                        code_language = "robot"
                    elif selected_framework == "Selenium + Cucumber (Java)":
                        code_language = "java"

                    st.code(automation_code, language=code_language)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Extract feature name for file naming
                    feature_name = "automated_test"
                    feature_match = re.search(
                        r"Feature:\s*(.+?)(?:\n|$)", st.session_state.generated_steps
                    )
                    if feature_match:
                        feature_name = (
                            feature_match.group(1).strip().replace(" ", "_").lower()
                        )

                    # Get appropriate file extension
                    file_ext = FRAMEWORK_EXTENSIONS[selected_framework]

                    # Add download button
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label=f"📥 Download {selected_framework} Code",
                            data=automation_code,
                            file_name=f"{feature_name}_automation.{file_ext}",
                            mime="text/plain",
                        )

                    st.markdown(
                        '<div class="status-success fade-in">Automation code generated successfully!</div>',
                        unsafe_allow_html=True,
                    )

                except Exception as e:
                    st.markdown(
                        f'<div class="status-error">Error generating {selected_framework} code: {str(e)}</div>',
                        unsafe_allow_html=True,
                    )

    # Footer
    st.markdown(
        '<div class="footer fade-in">© 2024 www.waigenie.tech | AI-Powered Test Automation</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</section>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
