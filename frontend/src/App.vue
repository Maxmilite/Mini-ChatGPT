<script setup lang="ts">
import { ref } from "vue";
import { ElMessage, messageEmits } from 'element-plus'

const state = ref(0);

function stateHandler(e: number) {
  state.value = e;
  if (e === 1) {
    ElMessage.success("A new chat session created.")
  }
}

const sleep = (delay: number) => new Promise((resolve) => setTimeout(resolve, delay));

async function submitMessage(message: string) {
  await sleep(2000);
  return "是的，" + message.replace("吗", "") + "。";
}

</script>

<template>
  <el-config-provider namespace="ep">
    <BaseHeader @response="(e) => stateHandler(e)" />
    <div style="display: flex">
      <BaseSide @response="(e) => stateHandler(e)" :state="state" />
      <div style="width: 100%; height: calc(100vh - 60px);">
        <Welcome v-if="state == 0" @response="(e) => stateHandler(e)" msg="Mini ChatGPT" />
        <ChatSession v-else :submit-function="submitMessage"/>
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
  