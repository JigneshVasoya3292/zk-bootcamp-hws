pragma solidity ^0.8.13;

// We will be implementing final checks of groth16 here

struct G1 {
    uint256 x;
    uint256 y;
}

struct G2 {
    uint256 x1;
    uint256 x2;
    uint256 y1;
    uint256 y2;
}


contract HW6 {
    uint256 constant FIELD_MODULUS = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
    G1 private G1_Point = G1({x : 1, y : 2});
    G1 private alpha1 = scalarMul(G1_Point, 5);
    
    // 6G2
    G2 private beta2 = G2(12345624066896925082600651626583520268054356403303305150512393106955803260718, 
                            10191129150170504690859455063377241352678147020731325090942140630855943625622, 
                            13790151551682513054696583104432356791070435696840691503641536676885931241944, 
                            16727484375212017249697795760885267597317766655549468217180521378213906474374);

    // 7G2
    G2 private gamma2 = G2(18551411094430470096460536606940536822990217226529861227533666875800903099477,
                            15512671280233143720612069991584289591749188907863576513414377951116606878472,
                            1711576522631428957817575436337311654689480489843856945284031697403898093784,
                            13376798835316611669264291046140500151806347092962367781523498857425536295743);

    // 25G2
    G2 private delta2 = G2(18610673905296475200012094379055809074803913595286370954927388508677460861790,
                            8291087306683232230307116604030965449129961501505521119497789796509253061829,
                            20420402523069121083407756226777154949751610360899848465783058166002212935791,
                            21841660452326164162844097646799750129318878235996004691585708530717715272524);

    function verify(G1 calldata a1, G2 calldata b2, G1 calldata c1, uint256 x1, uint256 x2, uint256 x3) public view returns (bool) {
        // X1 = x1G1 + x2G2 + x3G3
        G1 memory X1 = pointsAdd(scalarMul(G1_Point, x1), pointsAdd(scalarMul(G1_Point, x2), scalarMul(G1_Point, x3)));
        
        // -A1
        G1 memory negA1 = negate(a1);

        bytes memory payload = abi.encode(
            negA1.x,negA1.y,
            b2.x1,b2.x2,b2.y1,b2.y2,
            alpha1.x, alpha1.y,
            beta2.x1, beta2.x2, beta2.y1, beta2.y2,
            X1.x, X1.y,
            gamma2.x1, gamma2.x2, gamma2.y1, gamma2.y2,
            c1.x, c1.y,
            delta2.x1, delta2.x2, delta2.y1, delta2.y2
        );

        (bool ok, bytes memory result) = address(8).staticcall(payload);
        require(ok, "Pairings call failed");
        return abi.decode(result, (bool));
    }

    function scalarMul(G1 memory point, uint256 scalar) internal view returns(G1 memory) {
       (uint256 _x, uint256 _y) =  ecMul(point.x, point.y, scalar);
       return G1({
            x : _x,
            y: _y
       });
    }

    function pointsAdd(G1 memory p1, G1 memory p2) internal view returns(G1 memory) {
        (uint256 _x, uint256 _y) =  ecAdd(p1.x, p1.y, p2.x, p2.y);
        return G1({
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

    function negate(G1 memory g1) internal pure returns (G1 memory) {
        if (g1.x == 0 && g1.y == 0) {
            return G1(0, 0);
        } else {
            // whenever use points, We need FIELD_MODULUS so points stays within range of field, 
            // eg. In F13, all points (x, y) has range 0 to 12
            return G1(g1.x, (FIELD_MODULUS - g1.y) % FIELD_MODULUS);
        }
    }
}