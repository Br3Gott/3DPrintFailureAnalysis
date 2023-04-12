import styled from "styled-components"

const Container = styled.div`
    height: fit-content;
    margin-bottom: 10px;
    margin: 5px;

    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: #FaFaFa;
    box-shadow: 1px 1px 7px #bebebe,
               -1px -1px 7px #ffffff;
`
const SplitContainer = styled(Container)`
    justify-content: space-between;
    width: calc(100% - 10px);
    margin: 5px;

    box-shadow: 1px 1px 3px #bebebe,
               -1px -3px 5px #ffffff;
`

const ScrollableContainer = styled(Container)`
    height: 20em; 
    overflow-y: scroll;
`

export function StatusCard({ children }) {
    return (
        <Container>
            {children}
        </Container>
    )
}
export function StatusCardSplit({ children }) {
    return (
        <SplitContainer>
            {children}
        </SplitContainer>
    )
}
export function StatusCardScrollable({ children }) {
    return (
        <ScrollableContainer>
            {children}
        </ScrollableContainer>
    )
}