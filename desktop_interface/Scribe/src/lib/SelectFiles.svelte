<script lang="ts">
    import { open } from "@tauri-apps/api/dialog"
    let selectedFiles;
    $: selectedFiles
    
    const readFile = async () => {
        try {
            const selected = await open({
            multiple: true,
            title: "Open Video or Audio File"
            })
            selectedFiles = selected
        } catch (error) {
            console.log(error)
        }
    }
    if (Array.isArray(readFile)) {
    // user selected multiple files
    } else if (readFile === null) {
    // user cancelled the selection
    } else {
    // user selected a single file
    }
    
    function onSubmit(){
        // TODO need to send message to rust to load binary and run this file
    }

</script>

<label for="Files">Select MP4/MP3 Files</label>
<button on:click={readFile}>Open Files</button>
<button>Submit</button>
{#if selectedFiles}
    <p>{selectedFiles}</p>
{/if}
