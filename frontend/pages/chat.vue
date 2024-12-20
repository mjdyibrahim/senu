<template>
    <div>
        <Header />
        <section class="chat">
            <div class="chatbox-container" id="chatbox">
                <div class="chat-header" id="chat-header">
                    Chat with Senu, AI Copilot
                </div>
                <div class="chat-messages" id="chat-messages">
                    <!-- Messages will appear here -->
                </div>
                <div class="chat-input-container">
                    <input
                        type="text"
                        id="chat-input"
                        class="chat-input"
                        placeholder="Type your message here..."
                        v-model="message"
                        @keydown.enter="sendMessage"
                    />
                    <button class="send-button" @click="sendMessage">
                        Send
                    </button>
                </div>
            </div>
        </section>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";

export default {
    components: {
        Header,
        Footer,
    },
    data() {
        return {
            message: "",
        };
    },
    methods: {
        sendMessage() {
            // Handle sending message logic here
        },
    },
};
</script>

<style scoped>
/* Import main style */
</style>
