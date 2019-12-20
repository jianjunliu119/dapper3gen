<DataGrid x:Name="dataGrid" Height="600" ItemsSource="{Binding}" CanUserAddRows="False" AutoGenerateColumns="False">
    <DataGrid.Columns>
        <DataGridTextColumn Header="$header" Binding="{Binding $binding}"></DataGridTextColumn>
    </DataGrid.Columns>
</DataGrid>