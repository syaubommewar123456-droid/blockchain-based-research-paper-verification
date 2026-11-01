const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

const ABI = [
{
"inputs":[
{"internalType":"string","name":"_hash","type":"string"},
{"internalType":"string","name":"_owner","type":"string"}
],
"name":"addPaper",
"outputs":[],
"stateMutability":"nonpayable",
"type":"function"
},
{
"inputs":[
{"internalType":"string","name":"_hash","type":"string"}
],
"name":"getPaper",
"outputs":[
{"internalType":"string","name":"","type":"string"},
{"internalType":"string","name":"","type":"string"},
{"internalType":"uint256","name":"","type":"uint256"}
],
"stateMutability":"view",
"type":"function"
}
];

let signer;
let wallet;

document.getElementById("connectWallet").onclick = async () => {

    if (!window.ethereum) {
        alert("Install MetaMask");
        return;
    }

    await window.ethereum.request({
        method: "eth_requestAccounts"
    });

    const provider = new ethers.providers.Web3Provider(window.ethereum);

    signer = provider.getSigner();

    wallet = await signer.getAddress();

    document.getElementById("walletAddress").innerHTML =
        "Wallet : " + wallet;
};

document.getElementById("registerBlockchain").onclick = async () => {

    if (!signer) {
        alert("Connect wallet first");
        return;
    }

    const contract = new ethers.Contract(
        CONTRACT_ADDRESS,
        ABI,
        signer
    );

    document.getElementById("txStatus").innerHTML =
        "Waiting for MetaMask...";

    const tx = await contract.addPaper(
        PAPER_HASH,
        wallet
    );

    await tx.wait();

    document.getElementById("txStatus").innerHTML =
        "Research paper stored successfully on blockchain.";
};