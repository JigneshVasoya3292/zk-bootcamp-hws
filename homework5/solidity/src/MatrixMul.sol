pragma solidity ^0.8.13;

import { EcVerify } from "./EcVerify.sol";

struct ECPoint {
    uint256 x;
    uint256 y;
}

contract MatrixMul {
    function matrixmul(uint256[][] calldata matrix, uint256 n, ECPoint[] calldata s, uint256[] calldata o) public view returns (bool verified) {
        require(n != 0 && s.length != 0 || o.length != 0, "Invalid length for inputs");
        require(n == s.length, "Length of matrix don't match");

        ECPoint[] memory result = new ECPoint[](n);
        ECPoint memory G = ECPoint({ x: 1, y:2 });
        for(uint i = 0; i < n; i++) {
            result[i] = ECPoint({ x: 0, y:0});
            for(uint j = 0; j < n; j++) {
                uint256 scalar = matrix[i][j];
                ECPoint calldata point = s[j]; // todo : check if calldata can be used here
                result[i] = pointsAdd(result[i], scalarMul(point, scalar));
            }

            // compare with o
            ECPoint memory o_mul = scalarMul(G, o[i]);
            if(result[i].x != o_mul.x || result[i].y != o_mul.y) {
                return false;
            }
        }

        return true;
    }

    function scalarMul(ECPoint memory point, uint256 scalar) internal view returns(ECPoint memory) {
       (uint256 _x, uint256 _y) =  ecMul(point.x, point.y, scalar);
       return ECPoint({
            x : _x,
            y: _y
       });
    }

    function pointsAdd(ECPoint memory p1, ECPoint memory p2) internal view returns(ECPoint memory) {
        (uint256 _x, uint256 _y) =  ecAdd(p1.x, p1.y, p2.x, p2.y);
        return ECPoint({
            x : _x,
            y: _y
        });
    }

    function ecAdd(uint256 x1, uint256 y1, uint256 x2, uint256 y2) public view returns(uint256, uint256) {
        // 0x06 ecAdd precompile - https://www.evm.codes/precompiled?fork=osaka#0x06
        bytes memory payload = abi.encode(x1, y1, x2, y2);
        (bool ok, bytes memory result) = address(6).staticcall(payload);
        require(ok, "Failed during ecAdd call");
        return abi.decode(result, (uint256, uint256));
    }

    function ecMul(uint256 x1, uint256 y1, uint256 scalar) public view returns(uint256, uint256) {
        // 0x06 ecMul precompile - https://www.evm.codes/precompiled?fork=osaka#0x07
        bytes memory payload = abi.encode(x1, y1, scalar);
        (bool ok, bytes memory result) = address(7).staticcall(payload);
        require(ok, "Failed during ecMul call");
        return abi.decode(result, (uint256, uint256));
    }
}