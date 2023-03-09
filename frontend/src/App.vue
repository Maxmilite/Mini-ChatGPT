<script setup lang="ts">
import { ref } from "vue";
import { ElMessage, messageEmits } from 'element-plus'

const serverAddress = "http://localhost:5000"
const state = ref(0);

function stateHandler(e: number) {
  state.value = e;
  if (e === 1) {
    ElMessage.success("A new chat session created.")
  }
}

const sleep = (delay: number) => new Promise((resolve) => setTimeout(resolve, delay));

async function submitMessage(message: string) {
  let returnMessage = "";
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/message?message=" + message, false);
  try {
    HTTPRequest.send();
    returnMessage = HTTPRequest.responseText;
    return returnMessage;
  } catch (error) {
    return "An error occurred while corresponding with the chatbot."
  }
}

</script>

<template>
  <el-config-provider namespace="ep">
    <BaseHeader @response="(e) => stateHandler(e)" />
    <div style="display: flex">
      <BaseSide @response="(e) => stateHandler(e)" :state="state" />
      <div style="width: 100%; height: calc(100vh - 60px);">
        <Welcome v-if="state == 0" @response="(e) => stateHandler(e)" msg="Mini ChatGPT" />
        <ChatSession v-else :submit-function="submitMessage" />
      </div>
    </div>
  </el-config-provider>
</template>
  
<style>
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
}

.element-plus-logo {
  width: 50%;
}
</style>
