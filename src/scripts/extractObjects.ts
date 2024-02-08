// Import the mammoth library
import mammoth from 'mammoth';
import { OpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { getCookie } from './cookies';


// -----------------------------
// Extract objects from file
// -----------------------------

const initializeChain = () => {
	const llm = new OpenAI({
		openAIApiKey: getCookie("apikey") as string,
		modelName: "gpt-3.5-turbo-1106",
		temperature: .7,
	});

	let template = `Extract 1 or multiple objects from the following text written in Esperanto. Each object has the following properties
- tipo
- lando
- metalo
- diametro
- kvanto
- pezo
- artisto
- diko

If you don't have a value for a property, leave it as a null-value. Your answer HAS to be in json format following the following structure. Make sure it's immediately parsable as JSON:
{{
	'response': [
		{{
			'tipo': '',
			'lando': '',
			'metalo': '',
			'diametro': '',
			'kvanto': '',
			'pezo': '',
			'artisto': '',
			'diko': ''
		}},
		...
	]	
}}
<<input text>>
{text}	
	`

	console.log('Template:', template);

	let prompt = new PromptTemplate({
		inputVariables: ['text'],
		template: template,
	});

	const chain = prompt.pipe(llm);
	return chain;
}

const exportObjects = async (files: FileList) => {
	// TODO: Implement the extraction of objects from the files
	let found_objects: object[] = [];
	const chain: any = initializeChain(); // TODO: Initialize the OpenAI chain
	for (let i = 0; i < files.length; i++) {
		const file = files[i];
		if (isTemporaryFile(file.name)) {
			continue;
		}

		const objects = await extractObjects(file, chain);
		found_objects = found_objects.concat(objects);
	}

	console.log('Found objects:', found_objects);
	return found_objects;

};

async function extractObjects(file: File, chain: any): Promise<Object[]> {
	const html = await fileToHtml(file);
	const text = await docxfileToText(file);

	// TODO: Use LangChain to extract properties from the file
	let response: object[];
	// Perform a for loop of 3 to get the response from the chain
	for (let i = 0; i < 3; i++) {
		try {
			console.log(chain)
			let returned = await chain.invoke({ text });
			// Bring the response from a string to a JSON object
			console.log('Returned:', returned);
			response = JSON.parse(returned);
			console.log('Response:', response);
			break;
		
		}
		catch (e) {
			console.log('Error:', e);
		}
	}

	return [{ html, text }]; 
};

// -----------------------------
// Support functions
// -----------------------------
function isTemporaryFile(fileName: string): boolean {
	// Temporary Word files typically start with "~$" and end with ".docx"
	return fileName.startsWith('~$') && fileName.endsWith('.docx');
}

const fileToHtml = async (file: File) => {
	const result = await mammoth.convertToHtml(
		{ arrayBuffer: await file.arrayBuffer() },
		{ includeDefaultStyleMap: true }
	);

	let text = removeImages(result.value);
	return text;
};

const docxfileToText = async (file: File) => {
	const arrayBuffer = await file.arrayBuffer();
	const result = await mammoth.extractRawText({ arrayBuffer });
	return result.value;
};

const removeImages = (text: string) => {
	const regex = /<img[^>]+src="([^">]+)"/g;
	return text.replace(regex, '');
};


// Export
export default exportObjects;
