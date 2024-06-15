PYTHON_PATH =  ./.venv/scripts/python.exe

main: 
	@$(PYTHON_PATH) -m streamlit run main.py --server.headless True
