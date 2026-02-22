// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.30;

struct ECPoint {
    uint256 x;
    uint256 y;
}

contract EcVerify {
    uint256 constant CURVE_ORDER = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
    uint256 constant FIELD_MODULUS = 21888242871839275222246405745257275088696311157297823662689037894645226208583;

    // return true if the prover knows two numbers that add up to num/den
    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool verified) {
        
        require(den != 0, "denominator can not be 0");
        (uint256 ecSumX, uint256 ecSumY) = ecAdd(A.x, A.y, B.x, B.y);
        uint256 denInverse = modExp(den, CURVE_ORDER-2, CURVE_ORDER);
        uint256 multiplied = mulmod(num, denInverse, CURVE_ORDER);
        (uint256 scalarX, uint256 scalarY) = ecmul(1, 2, multiplied);
        if (ecSumX == scalarX && ecSumY == scalarY) {
            return true;
        } 

        return false;
    }

    function modExp(uint256 base, uint256 exp, uint256 mod) internal view returns (uint256) {
        // 0x05 modexp precompile - https://www.evm.codes/precompiled?fork=osaka#0x05
        bytes memory payload = abi.encode(32, 32, 32, base, exp, mod);
        (bool ok, bytes memory result) = address(5).staticcall(payload);
        require(ok, "Failed during modexp call");
        return abi.decode(result, (uint256));
    }

    function ecAdd(uint256 x1, uint256 y1, uint256 x2, uint256 y2) internal view returns(uint256, uint256) {
        // 0x06 ecAdd precompile - https://www.evm.codes/precompiled?fork=osaka#0x06
        bytes memory payload = abi.encode(x1, y1, x2, y2);
        (bool ok, bytes memory result) = address(6).staticcall(payload);
        require(ok, "Failed during ecAdd call");
        return abi.decode(result, (uint256, uint256));
    }

    function ecmul(uint256 x1, uint256 y1, uint256 scalar) internal view returns(uint256, uint256) {
        // 0x06 ecMul precompile - https://www.evm.codes/precompiled?fork=osaka#0x07
        bytes memory payload = abi.encode(x1, y1, scalar);
        (bool ok, bytes memory result) = address(7).staticcall(payload);
        require(ok, "Failed during ecMul call");
        return abi.decode(result, (uint256, uint256));
    }
}
