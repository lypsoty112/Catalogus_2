<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';

	export let exportedObjects: any[];

	let displayObjects = exportedObjects;

	let criteriaCount: number = 1;

	let counter: number = 0;
	const updateCounter = (): number => {
		counter += 1;
		return counter;
	};

	let sortingOptions: string[] = [
		'title',
		'artisto',
		'diametro',
		'diko',
		'kvanto',
		'lando',
		'metalo',
		'pezo',
		'tipo'
	];
	let sortingOrder: string[] = [sortingOptions[0]];

	function sortObjects(): void {
		console.log(sortingOrder);
		displayObjects = exportedObjects.sort((a, b) => {
			let result = 0;
			for (let i = 0; i < criteriaCount; i++) {
				const criteria = sortingOrder[i];
				let aCriteria = a.object[criteria] ? a.object[criteria] : 'ZZZZZ'; // If the criteria is not found, put it at the end of the list
				let bCriteria = b.object[criteria] ? b.object[criteria] : 'ZZZZZ'; // If the criteria is not found, put it at the end of the list
				if (aCriteria < bCriteria) {
					result = -1;
					break;
				} else if (aCriteria > bCriteria) {
					result = 1;
					break;
				}
			}
			return result;
		});

		counter = 0;
		displayObjects = [...displayObjects];
		console.log(displayObjects, sortingOrder);
	}

	function onSortChange(e: Event, index: number): void {
		const target = e.target as HTMLSelectElement;
		const value = target.value;

		sortingOrder[index] = value;
	}
</script>

<div class="w-4/6 my-4 mx-auto">
	<div class="my-2">
		{#each { length: criteriaCount } as _, i}
			<div class="my-1">
				<span class="text-lg">Criteria {i + 1}:</span>
				<select
					class="select"
					on:change={(e) => {
						onSortChange(e, i);
					}}
				>
					{#each sortingOptions as option}
						<option value={option}>Sorteer op {option}</option>
					{/each}
				</select>
			</div>
		{/each}
	</div>
	<div class="grid grid-cols-4">
		<div class="flex justify-center">
			<button class="btn variant-ghost-primary" on:click={sortObjects}>Sorteer</button>
		</div>
		<div class="flex justify-center">
			<button
				class="btn variant-ghost-error"
				on:click={() => {
					criteriaCount = 1;
					sortingOrder = [sortingOptions[0]];
				}}>Reset</button
			>
		</div>
		<div class="flex justify-center">
			<button
				class="btn variant-ghost-success"
				on:click={() => {
					criteriaCount++;
				}}>Voeg criteria toe</button
			>
		</div>
		<div class="flex justify-center">
			<button
				class="btn variant-ghost-success"
				on:click={() => {
					criteriaCount--;
					criteriaCount = criteriaCount < 1 ? 1 : criteriaCount;
				}}>Verwijder criteria</button
			>
		</div>
	</div>
</div>
<div>
	<div class="table-container">
		<table class="table table-hover">
			<thead>
				<tr>
					<th>Nummer</th>
					<th>Titel</th>
					<th>Artisto</th>
					<th>Diametro</th>
					<th>Diko</th>
					<th>Kvanto</th>
					<th>Lando</th>
					<th>Metalo</th>
					<th>Pezo</th>
					<th>Tipo</th>
				</tr>
			</thead>
			<tbody>
				{#each displayObjects as object}
					<tr>
						<td class=" font-bold">{updateCounter()}</td>
						<td>{object?.object?.title}</td>
						<td>{object?.object?.artisto}</td>
						<td>{object?.object?.diametro}</td>
						<td>{object?.object?.diko}</td>
						<td>{object?.object?.kvanto}</td>
						<td>{object?.object?.lando}</td>
						<td>{object?.object?.metalo}</td>
						<td>{object?.object?.pezo}</td>
						<td>{object?.object?.tipo}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
