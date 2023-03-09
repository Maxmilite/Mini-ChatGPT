<script setup lang="ts">
import { ElButton, ElMessage } from 'element-plus';
import "~/styles/index.scss";

import { onMounted, ref } from 'vue'
import { WordSpacingProperty } from 'csstype';
import { type } from 'os';
import { ElScrollbar } from 'element-plus'
import { update } from 'lodash';

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
  return [
    { value: '戴批是傻逼吗', link: 'https://www.sdu.edu.cn/' },
  ]
}

const MessageTemplate = {
  id: 0,
  message: ""
}

const messageList = ref([
  { id: 1, message: "I\'m a robot. You can chat with me freely now." },
]);

const props = defineProps({
  submitFunction: Function,
});

const innerChatBox = ref<HTMLDivElement>();
const chatBoxRef = ref<InstanceType<typeof ElScrollbar>>();

const submitLoading = ref(false);

async function submit() {

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

  messageList.value.push({ id: 0, message: message });
  submitLoading.value = true;
  updateChatBoxHeight();

  let response = await props.submitFunction(message);
  messageList.value.push({ id: 1, message: response });
  updateChatBoxHeight();

  submitLoading.value = false;
  
}

const updateChatBoxHeight = () => {
  setTimeout(() => chatBoxRef.value!.setScrollTop(innerChatBox.value!.clientHeight), 10);
}

onMounted(() => {
  words.value = loadAll();
  updateChatBoxHeight();
})

</script>

<template>
  <el-container style="height: calc(100vh - 100px);">
    <el-main>
      <el-scrollbar max-height="calc(100vh - 100px)" ref="chatBoxRef">
        <div ref="innerChatBox">
          <div v-for="item in messageList">
            <p v-if="item.id === 0" class="scrollbar-self">{{ item.message }}</p>
            <p v-else class="scrollbar-chatbot">{{ item.message }}</p>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer>
      <el-row>
        <el-col :span="16">
          <el-autocomplete style="margin: 0 0;" v-model="search_state" :fetch-suggestions="querySearch" clearable
            type="textarea" :autosize="{ minRows: 1, maxRows: 3 }" class="inline-input search-bar w-50vw" size="large"
            placeholder="Type any words freely. Use Ctrl + Enter to submit." :disabled="submitLoading" @keyup.ctrl.enter="submit" />
        </el-col>
        <el-col :span="8">
          <el-button id="submit-button" :loading="submitLoading" style="margin: 0 0;" type="primary"  plain
            @click="submit">Submit</el-button>
        </el-col>
      </el-row>
    </el-footer>
  </el-container>
</template>

<style scoped>
.scrollbar-self {
  display: flex;
  align-items: center;
  justify-content: left;
  min-height: 60px;
  text-align: center;
  border-radius: 4px;
  background: #18222c;
  color: #409eff;
  margin-left: calc(max(100vw - 500px, 50vw));
  margin-top: 20px;
  padding: 5px 20px;
}

.scrollbar-chatbot {
  display: flex;
  align-items: center;
  justify-content: left;
  min-height: 60px;
  text-align: center;
  border-radius: 4px;
  background: #1c2518;
  color: #67c23a;
  margin-right: calc(max(100vw - 500px, 50vw));
  margin-top: 20px;
  padding: 5px 20px;
}
</style>