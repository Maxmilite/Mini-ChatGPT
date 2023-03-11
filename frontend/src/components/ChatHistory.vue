<script setup lang="ts">
import { ElButton, ElMessage } from 'element-plus';
import "~/styles/index.scss";
import 'uno.css'
import "element-plus/theme-chalk/src/message.scss"
import "~/styles/chat-session.scss"

import { onMounted, ref } from 'vue'
import { ElScrollbar } from 'element-plus'

const props = defineProps({
  historyFunction: Function,
  category: String
});

interface WordItem {
  question: string,
  answer: string,
  date: Date,
  category: string,
  id: number
}

const words = ref<WordItem[]>([])
const loadAll = () => {
  let res = props.historyFunction!(props.category);
  return res;
}

const innerChatBox = ref<HTMLDivElement>();
const chatBoxRef = ref<InstanceType<typeof ElScrollbar>>();


onMounted(() => {
  words.value = loadAll();
})

</script>

<template>
  <el-container style="height: calc(100vh - 60px);">
    <el-main id="chatbox-main">
      <el-scrollbar ref="chatBoxRef">
        <div ref="innerChatBox">
          <div v-for="item in words">
            <p class="scrollbar-self">{{ item.question }}</p>
            <p class="scrollbar-chatbot">{{ item.answer }}</p>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
  </el-container>
</template>
