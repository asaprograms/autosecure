// lunarclient_ws_fetch.js
// only if the lunarclient websocket was installed
const { LunarClient } = require('lunarclient-websocket');

async function main() {
    const accessToken = process.argv[2];
    if (!accessToken) {
        console.error(JSON.stringify({ success: false, error: 'Access token is required' }));
        process.exit(1);
    }
    const client = new LunarClient();
    try {
        await client.connect(accessToken);
        const cosmetics = client.getCosmetics();
        const emotes = client.getEmotes();
        console.log(JSON.stringify({ success: true, data: { cosmetics, emotes } }));
    } catch (err) {
        const errorMessage = err?.message || err?.toString() || 'Unknown error occurred';
        console.error(JSON.stringify({ success: false, error: errorMessage }));
        process.exit(1);
    } finally {
        client.disconnect();
    }
}

main(); 