var Lottereum = artifacts.require("Lottereum");

module.exports = function(deployer) {
  deployer.deploy(Lottereum, 1, 10, 10, 5, 1 hour);
}
