import ModuleContainer from "../ModuleContainer"
import styled from "styled-components"
import { StatusCard, StatusCardScrollable } from "../StatusCard"


const PresetLayout = styled.div`
    width: 100%;
    height: fit-content;
`

const SliderLayout = styled.div`
    width: 100%;
    height: fit-content;

    label {
        float: left;
    }
    input {
        float: right;
    }
`

function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (arguments.length === 1) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}

function PresetDisplay({ lowHSV, highHSV }) {
    let c = HSVtoRGB(lowHSV[0] / 255, lowHSV[1] / 255, lowHSV[2] / 255)
    let containerStyle = {
        color: "rgb(" + c.r + "," + c.g + "," + c.b + ")"
    }

    return <p style={containerStyle}>{c.r} {c.g} {c.b} {highHSV}</p>
}

function PresetSelector() {
    const Presets = [
        [
            [101, 150, 132], [255, 255, 255]
        ]
    ]

    return (
        <PresetLayout>
            {Presets.map(preset => {
                return <PresetDisplay lowHSV={preset[0]} highHSV={preset[1]} />
            })}
        </PresetLayout>
    )
}

export default function FilterSettings({ lowHSV, highHSV, handleChange }) {

    function sendHandleChange(e) {
        handleChange(e.target.id, e.target.value)
    }

    return (
        <ModuleContainer>
            <StatusCard>
                Filter Settings
            </StatusCard>
            <StatusCard>
                <PresetSelector />
                <SliderLayout>
                    <StatusCard>
                        <label htmlFor="low_h">Low Hue: {lowHSV[0]}</label>
                        <input id="low_h" value={lowHSV[0]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>
                    <StatusCard>
                        <label htmlFor="low_s">Low Saturation: {lowHSV[1]}</label>
                        <input id="low_s" value={lowHSV[1]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>
                    <StatusCard>
                        <label htmlFor="low_v">Low Value: {lowHSV[2]}</label>
                        <input id="low_v" value={lowHSV[2]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>

                    <StatusCard>
                        <label htmlFor="high_h">High Hue: {highHSV[0]}</label>
                        <input id="high_h" value={highHSV[0]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>
                    <StatusCard>
                        <label htmlFor="high_s">High Saturation: {highHSV[1]}</label>
                        <input id="high_s" value={highHSV[1]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>
                    <StatusCard>
                        <label htmlFor="high_v">High Value: {highHSV[2]}</label>
                        <input id="high_v" value={highHSV[2]} type="range" min="0" max="255" onChange={sendHandleChange} /> <br />
                    </StatusCard>
                </SliderLayout>
            </StatusCard>
        </ModuleContainer>
    )
}