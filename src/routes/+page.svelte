<script lang="ts">
	import { Stepper, Step, FileButton } from '@skeletonlabs/skeleton';
	import Loader from '../components/loader.svelte';
	import exportObjects from '../scripts/extractObjects';
	import SortApp from './sortApp.svelte';

	let allFiles: FileList;
	let loading_2: boolean = true;
	let exportedObjects: Object[];

	$: lockFirstStep = allFiles?.length === 0 || allFiles === undefined;

	async function onStepHandler(e: {
		detail: { state: { current: number; total: number }; step: number };
	}): Promise<void> {
		if (e.detail.state.current === 1) {
			exportedObjects = await exportObjects(allFiles);
			console.log(exportedObjects);
			console.log(allFiles);
			loading_2 = false;
		} else {
			loading_2 = true;
		}
	}
</script>

<div class="container p-4 mx-auto">
	<div class="card variant-ghost-surface w-full p-8">
		<Stepper on:next={onStepHandler}>
			<Step locked={lockFirstStep}>
				<svelte:fragment slot="header">Upload de folder die alle documenten inhoud</svelte:fragment>
				<div class="flex justify-center">
					<FileButton
						bind:files={allFiles}
						name="files"
						button="btn btn-xl variant-filled-primary"
						webkitdirectory>Kies folder</FileButton
					>
				</div>
				<div class="flex justify-center">
					<span>
						{#if allFiles?.length > 0}
							{allFiles.length} bestanden geselecteerd
						{:else}
							Geen bestanden geselecteerd
						{/if}
					</span>
				</div>
				<svelte:fragment slot="navigation">
					<button
						class="btn variant-ghost-error"
						on:click={() => {
							window.location.reload();
						}}>Reset</button
					>
				</svelte:fragment>
			</Step>
			<Step>
				<svelte:fragment slot="header">Sorteer de documenten</svelte:fragment>
				<div>
					{#if loading_2}
						<div class="flex justify-center">
							<Loader />
						</div>
						<div class="flex justify-center">
							<span class=" text-xl font-bold"
								>Nu uw bestanden aan het bekijken, even wachten..</span
							>
						</div>
					{:else}
						<SortApp {exportedObjects} />
					{/if}
				</div>
			</Step>
			<Step>
				<svelte:fragment slot="header">Download het samengevoegde document</svelte:fragment>
				(content)
			</Step>
			<!-- ... -->
		</Stepper>
	</div>
</div>
