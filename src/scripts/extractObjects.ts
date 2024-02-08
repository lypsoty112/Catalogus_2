// Import the mammoth library
import mammoth from 'mammoth';
// -----------------------------
// Extract objects from file
// -----------------------------
const extractObjectsFromFile = async (file: File) => {
	let objectsFound = [];
	const html = await fileToHtml(file);
	const text = await docxfileToText(file);

	// Count the amount of tipo occurrences
	const tipoRegex = /tipo/gi;
	const tipoCount = (text.toLowerCase().match(tipoRegex) || []).length;
	// Find the titles
	const fileObject = {
		name: file.name,
		size: file.size,
		type: file.type,
		html: html,
		text: text,
		tipoCount: tipoCount
	};

	if (tipoCount < 2) {
		// If there are less than 2 tipo occurrences, the file is 1 object
		// Title is the first line of the text
		const title = text.split('\n')[0];
		const object = {
			text: text,
			html: html
		};
		return [
			{
				file: fileObject,
				object: {
					title: title,
					...object,
					...extractObjectProperties(object)
				}
			}
		];
	} else {
		const titles = extractTitles(text);
		const objects = extractObjectTexts(text, html, titles);
		for (let i = 0; i < titles.length; i++) {
			const title = titles[i];
			const object = objects[i];

			objectsFound.push({
				file: fileObject,
				object: {
					title: title,
					...object,
					...extractObjectProperties(object)
				}
			});
		}
		return objectsFound;
	}
};

const exportObjects = async (files: FileList) => {
	// Iterate over each file
	// Filter out temporary docx files

	let objects = [];

	const filesWithout = Array.from(files).filter((file) => !isTemporaryFile(file.name));

	for (let i = 0; i < filesWithout.length; i++) {
		// Read the file
		let file = filesWithout[i];
		objects.push(...(await extractObjectsFromFile(file)));
	}

	// Strip all values
	objects = objects.map((object) => {
		for (const [key, value] of Object.entries(object.object)) {
			object.object[key] = typeof value == 'string' ? value.trim() : value;
		}
		return object;
	});
	return objects;
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

const extractTitles = (text: string) => {
	const lines = text.split('\n');
	let titles = [];
	let previousLine = '';
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		if (line.toLowerCase().includes('tipo')) {
			titles.push(previousLine.trim());
		}
		previousLine = line == '' ? previousLine : line;
	}
	return titles;
};

const extractObjectTexts = (text: string, html: string, titles: any) => {
	// Split the text and the html into objects based on the titles
	// The first object is the first title until the second title
	// The second object is the second title until the third title
	// etc.
	// The last object is the last title until the end of the text or html

	// Initialize an empty array to store the objects
	let objects: any[] = [];

	// Loop through the titles array
	for (let i = 0; i < titles.length; i++) {
		// Get the current title and the next title
		let currentTitle = titles[i];
		let nextTitle = titles[i + 1];

		// Find the index of the current title and the next title in the text and html
		let textCurrentIndex = text.indexOf(currentTitle);
		let textNextIndex = nextTitle ? text.indexOf(nextTitle) : text.length;
		let htmlCurrentIndex = html.indexOf(currentTitle);
		let htmlNextIndex = nextTitle ? html.indexOf(nextTitle) : html.length;

		// Extract the substring between the current index and the next index for both text and html
		let textSubstring = text.substring(textCurrentIndex, textNextIndex);
		let htmlSubstring = html.substring(htmlCurrentIndex, htmlNextIndex);

		// Create an object with the title and the substrings as properties
		let object = {
			text: textSubstring,
			html: htmlSubstring
		};

		// Push the object to the array
		objects.push(object);
	}

	// Return the array of objects
	return objects;
};

const extractObjectProperties = ({ html, text }: { html: string; text: string }) => {
	// Properties to find: tipo, Lando, Metalo, Diametro, Kvanto, Pezo, Artisto / medalisto
	// Initialize an empty object to store the properties
	let properties: any = {
		tipo: null,
		lando: null,
		metalo: null,
		diametro: null,
		kvanto: null,
		pezo: null,
		artisto: null,
		diko: null
	};
	// Find the properties in the html
	let hmtlLowerCase = html.toLowerCase();
	// Every property is preceded by a > and followed by a <
	// The property value is between the > and the <
	// The property name is between the > and the :
	// The property name is followed by a space
	// The property value is followed by a space
	// The property value is followed by a <
	// The property value is followed by a <br> or a </p>

	const regexes = {
		tipo: /tipo ([^<]+)</,
		lando: /lando: ([^<]+)</,
		metalo: /metalo: ([^<]+)</,
		diametro: /diametro: ([^<]+)</,
		kvanto: /kvanto: ([^<]+)</,
		pezo: /pezo: ([^<]+)</,
		artisto: /medalisto: ([^<]+)</,
		diko: /diko: ([^<]+)</
	};

	for (const [key, value] of Object.entries(regexes)) {
		let match = hmtlLowerCase.match(value);
		if (match) {
			// Cut the match at '\' characters and '\t' characters
			properties[key] = match[1].split('\\')[0].split('\t')[0].trim();
		}
	}
	// Print the properties
	return properties;
};

// Export
export default exportObjects;