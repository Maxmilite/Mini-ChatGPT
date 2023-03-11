<script setup lang="ts">
import { ElButton, ElMessage } from 'element-plus';
import "~/styles/index.scss";
import 'uno.css'
import "element-plus/theme-chalk/src/message.scss"
import "~/styles/chat-session.scss"

import { onMounted, ref } from 'vue'
import { ElScrollbar } from 'element-plus'

const props = defineProps({
  submitFunction: Function,
  autoCompleteListFunction: Function
});

interface WordItem {
  value: string
}

const search_state = ref('')

const words = ref<WordItem[]>([])
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? words.value.filter(createFilter(queryString))
    : words.value
  cb(results)
}
const createFilter = (queryString: string) => {
  return (word: WordItem) => {
    return (
      word.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1
    )
  }
}
const loadAll = () => {
  let res = props.autoCompleteListFunction === undefined ? [] : props.autoCompleteListFunction();
  return res;
}

const MessageTemplate = {
  id: 0,
  message: ""
}

const messageList = ref([
  { id: 1, message: "I\'m a robot. You can chat with me freely now." },
]);


const innerChatBox = ref<HTMLDivElement>();
const chatBoxRef = ref<InstanceType<typeof ElScrollbar>>();

const submitLoading = ref(false);

function submit() {

  if (props.submitFunction === undefined)
    return;
  let submitButton = document.getElementById("submit-button");
  if (submitButton === null)
    return;
  let message = search_state.value;
  search_state.value = "";


  if (!message) {
    ElMessage.info("You need to type some words.");
    return;
  }

  submitLoading.value = true;
  messageList.value.push({ id: 0, message: message });
  updateChatBoxHeight();

  props.submitFunction(message, receiveMessage);
  
}

const receiveMessage = (result: string) => {
  messageList.value.push({ id: 1, message: result });
  updateChatBoxHeight();
  submitLoading.value = false;
}

const updateChatBoxHeight = () => {
  setTimeout(() => chatBoxRef.value!.setScrollTop(innerChatBox.value!.clientHeight));
}

onMounted(() => {
  words.value = loadAll();
  updateChatBoxHeight();
  ElMessage.success("A new chat session created.");
})

</script>

<template>
  <el-container style="height: calc(100vh - 60px);">
    <el-main id="chatbox-main">
      <el-scrollbar ref="chatBoxRef">
        <div ref="innerChatBox">
          <div v-for="item in messageList">
            <p v-if="item.id === 0" class="scrollbar-self">{{ item.message }}</p>
            <p v-else class="scrollbar-chatbot">{{ item.message }}</p>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer
      height="100px" 
      style="padding: 0 0; display: flex; align-items: center; justify-content: center; border: 1px solid var(--ep-border-color); border-radius: 3px; height: 120px margin-bottom: 0">
      <el-row
        style="display: flex; width: 100%; height: 100%; margin: 0 0; flex-direction: column; justify-content: center; align-items: center;">
        <el-col style="display: flex; justify-content: center; align-items: center;">
          <el-autocomplete style="margin: 0 0;" v-model="search_state" :fetch-suggestions="querySearch" clearable
            type="textarea" :autosize="{ minRows: 1, maxRows: 3 }" class="inline-input search-bar w-50vw" size="large"
            placeholder="Type any words freely. Use Ctrl + Enter to submit." :disabled="submitLoading"
            @keyup.ctrl.enter="submit" />
        </el-col>
        <el-col style="display: flex; justify-content: center; align-items: center;">
          <el-button id="submit-button" :loading="submitLoading" style="margin: 0 0;" type="primary" plain
            @click="submit">Submit</el-button>
        </el-col>
      </el-row>
    </el-footer>
  </el-container>
</template>
