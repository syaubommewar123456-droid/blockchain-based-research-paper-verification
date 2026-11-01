const hre = require("hardhat");

async function main() {
  const ResearchOwnership = await hre.ethers.getContractFactory("ResearchOwnership");

  const contract = await ResearchOwnership.deploy();

  await contract.deployed();

  console.log("=================================");
  console.log("Contract deployed successfully!");
  console.log("Contract Address:", contract.address);
  console.log("=================================");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });