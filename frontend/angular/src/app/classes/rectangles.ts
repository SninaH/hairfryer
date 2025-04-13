export class Rectangles {
    throw_order: number[] = []; // Initialize as an empty array
    pins_fallen_in_throw: number[] = []; // Initialize as an empty array
    pins_fallen_on_lane: number[] = []; // Initialize as an empty array
    pins: {
        pin_1: number[];
        pin_2: number[];
        pin_3: number[];
        pin_4: number[];
        pin_5: number[];
        pin_6: number[];
        pin_7: number[];
        pin_8: number[];
        pin_9: number[];
    } = {
        pin_1: [],
        pin_2: [],
        pin_3: [],
        pin_4: [],
        pin_5: [],
        pin_6: [],
        pin_7: [],
        pin_8: [],
        pin_9: [],
    }; // Initialize each pin as an empty array
}