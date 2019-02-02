package pl.dkolaczynski.alerter;

import javafx.application.Application;
import javafx.scene.control.Alert;
import javafx.stage.Stage;

public class Alerter extends Application {

	public static void main(String... args) {
		launch(args);
	}

	@Override
	public void start(Stage stage) {
		Alert alert = new Alert(Alert.AlertType.INFORMATION);
		alert.setTitle(getParameters().getNamed().get("title"));
		alert.setHeaderText(null);
		alert.setContentText(getParameters().getNamed().get("content"));

		alert.showAndWait();
	}

}
