<template>
    <div class="flex flex-col justify-start gap-0.5 py-1">
        <h3 class="font-medium">Pick Model:</h3>
        <select class="rounded-md h-8 p-1 w-[95%] outline-none">
            <optgroup label="Groq">
                <option>Gemma2-9b-it</option>
                <option>Gemma-7b-it</option>
                <option>llama-3.1-70b-versatile</option>
                <option>llama-3.1-8b-instant</option>
            </optgroup>
        </select>
    </div>
</template>
<script>
export default {
    
}
</script>