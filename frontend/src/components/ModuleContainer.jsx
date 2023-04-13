import styled from "styled-components"

const Container = styled.div`
    height: 100%;
    width: 30em;

    margin: auto;
    padding: 10px;

    background-color: white;
    border-radius: 10px;

    color: black;
`

export default function ModuleContainer({ children }) {
    return (
        <Container>
            {children}
        </Container>
    )
}