<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';

	export let exportedObjects: any[];

	let displayObjects = exportedObjects;

	let criteriaCount: number = 1;

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
	<ol class="list">
		{#each displayObjects as object, i}
			<li class="p-1 m-1 !rounded-lg variant-ghost-primary">
				<span>{i + 1}.</span>
				<span class="flex-auto">
					<Accordion>
						<AccordionItem>
							<svelte:fragment slot="summary">{object?.object?.title}</svelte:fragment>
							<svelte:fragment slot="content">
								<ul>
									<li class="my-1">
										<span class="font-bold">Artisto:</span>
										{#if object?.object?.artisto}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.artisto}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Diametro:</span>
										{#if object?.object?.diametro}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.diametro}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Diko:</span>
										{#if object?.object?.diko}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.diko}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Kvanto:</span>
										{#if object?.object?.kvanto}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.kvanto}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Lando:</span>
										{#if object?.object?.lando}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.lando}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Metalo:</span>
										{#if object?.object?.metalo}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.metalo}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Pezo:</span>
										{#if object?.object?.pezo}
											<span class="variant-filled-success rounded-lg px-2"
												>{object?.object?.pezo}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
									<li class="my-1">
										<span class="font-bold">Tipo:</span>
										{#if object?.object?.tipo}
											<span class="variant-filled-success rounded-lg px-2 px-2"
												>{object?.object?.tipo}</span
											>
										{:else}
											<span class="italic variant-filled-warning rounded-lg px-2 px-2"
												>Niet gevonden</span
											>
										{/if}
									</li>
								</ul>
							</svelte:fragment>
						</AccordionItem>
					</Accordion>
				</span>
			</li>
		{/each}
	</ol>
</div>
