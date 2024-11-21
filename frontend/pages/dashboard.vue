<template>
    <div>
        <Header />
        <main class="main-content">
            <section class="dashboard">
                <h2>Startup Dashboard</h2>
                <div id="burn-rate-graph" class="plotly-graph"></div>
                <div id="clv-graph" class="plotly-graph"></div>
                <div id="cac-graph" class="plotly-graph"></div>
                <div id="valuation-graph" class="plotly-graph"></div>
                <div id="exit-potential-graph" class="plotly-graph"></div>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
import Header from "~/components/Header/Header.vue";
import Footer from "~/components/Footer/Footer.vue";
import Plotly from "plotly.js-dist";

export default {
    components: {
        Header,
        Footer,
    },
    mounted() {
        // Burn Rate Graph
        var burnRateData = // Fetch data from your backend or use static data
            Plotly.newPlot("burn-rate-graph", burnRateData);

        // Customer Lifetime Value (CLV) Graph
        var clvData = // Fetch data from your backend or use static data
            Plotly.newPlot("clv-graph", clvData);

        // Customer Acquisition Cost (CAC) Graph
        var cacData = // Fetch data from your backend or use static data
            Plotly.newPlot("cac-graph", cacData);

        // Valuation Graph
        var valuationData = // Fetch data from your backend or use static data
            Plotly.newPlot("valuation-graph", valuationData);

        // Exit Potential Graph
        var exitPotentialData = // Fetch data from your backend or use static data
            Plotly.newPlot("exit-potential-graph", exitPotentialData);
    },
};
</script>

<style scoped>
/* Import main style */
@import "@/assets/css/main.css";
</style>
