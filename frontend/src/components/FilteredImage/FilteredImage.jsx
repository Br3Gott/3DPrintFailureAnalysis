import ModuleContainer from "../ModuleContainer"
import { useState } from "react"
import { OpenCvProvider, useOpenCv } from 'opencv-react'
import TestImage from '../../assets/testimage2.jpg'

export default function FilteredImage({ low_hsv, high_hsv }) {

    return (
        <ModuleContainer>
            <OpenCvProvider>
                <img id="inputImg" style={{ display: "none" }} src={TestImage} />
                <CV low_hsv={low_hsv} high_hsv={high_hsv} />
            </OpenCvProvider>
        </ModuleContainer>
    )
}

function CV({ low_hsv, high_hsv }) {
    const { loaded, cv } = useOpenCv()

    if (cv) {
        try {
            var c = document.getElementById("canvasInput")
            var ctx = c.getContext("2d")
            var image = document.getElementById("inputImg")
            ctx.drawImage(image, 0, 0, 400, 300)

            let src = cv.imread('canvasInput');
            cv.rotate(src, src, cv.ROTATE_180)

            let hsv = new cv.Mat();
            cv.cvtColor(src, hsv, cv.COLOR_BGR2HSV)
            
            console.log(low_hsv, high_hsv)

            let low = cv.matFromArray(hsv.rows, hsv.cols, hsv.type(), low_hsv);
            let high = cv.matFromArray(hsv.rows, hsv.cols, hsv.type(), high_hsv);

            let dst = new cv.Mat();
            cv.inRange(hsv, low, high, dst)

            cv.imshow('canvasOutput', dst);
            src.delete();
            dst.delete();
        }
        catch (error) {
            console.log("Error")
            console.log(error)
        }
    }



    return (
        <>
            <canvas width="400px" height="300px" style={{ display: "none" }} id="canvasInput" />
            <canvas id="canvasOutput" />
            <p>{cv ? 'Finished loading opencv library.' : 'Loading opencv library.'}</p>
        </>
    )
}